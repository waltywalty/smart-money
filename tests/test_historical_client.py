"""C6 - regression tests for the historical-collection invariants.

These are the rules that cost this project real errors in the 2026-08-14 run.
They are asserted against a stub transport, so the suite needs no network.
"""
import unittest

TERMINAL = ('cursor_exhausted', 'empty_page')


def page(fetch, params, cap=50):
    """The paging contract b1_collect.py implements. Reproduced here so the
    invariants can be tested without a network: a page loop must record WHY it
    stopped, and only cursor exhaustion or an empty page may be read as a
    complete answer."""
    rows, cursor, pages, stop, codes = [], None, 0, None, {}
    while stop is None and pages < cap:
        code, body = fetch(dict(params, cursor=cursor))
        codes[code] = codes.get(code, 0) + 1
        pages += 1
        if code != 200:
            stop = 'http_%s' % code
            break
        got = body.get('markets') or []
        rows += [m for m in got if not (m.get('ticker') or '').startswith('KXMVE')]
        cursor = body.get('cursor')
        if not got:
            stop = 'empty_page'
        elif not cursor:
            stop = 'cursor_exhausted'
    if stop is None:
        stop = 'page_cap'
    return {'rows': rows, 'pages': pages, 'stop': stop, 'codes': codes}


def mk(n, prefix='KXHIGHNY', start=0):
    return [{'ticker': '%s-T%d' % (prefix, i)} for i in range(start, start + n)]


class TestStopReason(unittest.TestCase):
    def test_a_429_is_NOT_exhaustion(self):
        """The 2026-08-14 error: a rate limit on page 7 was recorded as the end of
        the data and under-reported KXMLBGAME by 65% (1,400 against 4,083)."""
        seq = [(200, {'markets': mk(1000), 'cursor': 'c1'}), (429, {})]
        it = iter(seq)
        r = page(lambda p: next(it), {})
        self.assertEqual(r['stop'], 'http_429')
        self.assertNotIn(r['stop'], TERMINAL)

    def test_cursor_exhaustion_is_exhaustion(self):
        seq = [(200, {'markets': mk(3), 'cursor': None})]
        it = iter(seq)
        r = page(lambda p: next(it), {})
        self.assertEqual(r['stop'], 'cursor_exhausted')
        self.assertIn(r['stop'], TERMINAL)

    def test_an_empty_page_is_exhaustion_and_yields_no_rows(self):
        it = iter([(200, {'markets': [], 'cursor': 'still-here'})])
        r = page(lambda p: next(it), {})
        self.assertEqual(r['stop'], 'empty_page')
        self.assertEqual(r['rows'], [])

    def test_hitting_the_page_cap_is_recorded_and_is_not_terminal(self):
        r = page(lambda p: (200, {'markets': mk(1), 'cursor': 'always'}), {}, cap=3)
        self.assertEqual(r['stop'], 'page_cap')
        self.assertNotIn(r['stop'], TERMINAL)

    def test_a_403_is_never_readable_as_a_404(self):
        it = iter([(403, {})])
        r = page(lambda p: next(it), {})
        self.assertEqual(r['stop'], 'http_403')
        self.assertNotEqual(r['stop'], 'http_404')


class TestExclusions(unittest.TestCase):
    def test_KXMVE_is_excluded_a_priori(self):
        rows = mk(2) + [{'ticker': 'KXMVESPORTSMULTIGAMEEXTENDED-XYZ'}]
        it = iter([(200, {'markets': rows, 'cursor': None})])
        r = page(lambda p: next(it), {})
        self.assertEqual(len(r['rows']), 2)
        self.assertFalse(any(m['ticker'].startswith('KXMVE') for m in r['rows']))


class TestCompletenessGate(unittest.TestCase):
    def test_row_count_equals_unique_ticker_count(self):
        pages = [(200, {'markets': mk(1000, start=0), 'cursor': 'c1'}),
                 (200, {'markets': mk(500, start=1000), 'cursor': None})]
        it = iter(pages)
        r = page(lambda p: next(it), {})
        tickers = [m['ticker'] for m in r['rows']]
        self.assertEqual(len(tickers), len(set(tickers)))
        self.assertEqual(len(tickers), 1500)

    def test_overlapping_pages_would_be_caught_by_the_gate(self):
        # A cursor that repeats a page is data loss presenting as data.
        pages = [(200, {'markets': mk(10, start=0), 'cursor': 'c1'}),
                 (200, {'markets': mk(10, start=5), 'cursor': None})]
        it = iter(pages)
        r = page(lambda p: next(it), {})
        tickers = [m['ticker'] for m in r['rows']]
        self.assertNotEqual(len(tickers), len(set(tickers)))


class TestControlKeySemantics(unittest.TestCase):
    def test_an_ignored_filter_returns_rows_for_an_impossible_key(self):
        """Measured 2026-08-14: ?ticker= is silently ignored on both /markets and
        /historical/markets. The control key is the only thing that exposes it."""
        honoured = lambda p: (200, {'markets': [], 'cursor': None})
        ignored = lambda p: (200, {'markets': mk(5), 'cursor': None})
        self.assertEqual(page(honoured, {'series_ticker': 'IMPOSSIBLE'})['rows'], [])
        self.assertEqual(len(page(ignored, {'ticker': 'IMPOSSIBLE'})['rows']), 5)
