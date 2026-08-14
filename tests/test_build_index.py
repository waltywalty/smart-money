"""C6 - regression tests for scripts/build_index.py.

The index is generated and hypotheses.json is authoritative, so the risk here is
silent mangling: a verdict echo stripped into a dangling conjunction, a stale
bucket hidden instead of marked, or H9 sorting after H10.
"""
import os, sys, unittest
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import build_index as bi


class TestHNum(unittest.TestCase):
    def test_sorts_numerically_not_lexically(self):
        ids = ['H10', 'H9', 'H2', 'H64', 'H7']
        self.assertEqual(sorted(ids, key=bi.hnum), ['H2', 'H7', 'H9', 'H10', 'H64'])

    def test_survives_a_non_numeric_id(self):
        self.assertEqual(bi.hnum('HXX'), 0)


class TestVerdictEcho(unittest.TestCase):
    def test_strips_a_leading_echo_before_a_new_sentence(self):
        self.assertEqual(bi.ECHO.sub('', 'KILLED. The purest statement of the finding.'),
                         'The purest statement of the finding.')

    def test_does_NOT_strip_when_a_conjunction_follows(self):
        # "KILLED, and the most informative death" must not become a fragment.
        s = 'KILLED, and the most informative death in the registry'
        self.assertEqual(bi.ECHO.sub('', s), s)

    def test_leaves_an_unprefixed_line_alone(self):
        s = 'The band exists at ten minutes. It does not pay.'
        self.assertEqual(bi.ECHO.sub('', s), s)


class TestOneLine(unittest.TestCase):
    def test_returns_a_dash_when_no_field_is_populated(self):
        self.assertEqual(bi.one_line({}), '—')

    def test_truncates_with_an_ellipsis_and_respects_the_width(self):
        long = {f: 'x' * 4000 for f in bi.ONE_LINE_FIELDS[:1]}
        out = bi.one_line(long)
        self.assertLessEqual(len(out), bi.W_ONE)
        self.assertTrue(out.endswith('…'))

    def test_collapses_internal_whitespace(self):
        e = {bi.ONE_LINE_FIELDS[0]: 'a\n\n  b\tc'}
        self.assertEqual(bi.one_line(e), 'a b c')


class TestSupersededBy(unittest.TestCase):
    def test_marks_a_bucket_that_contradicts_its_own_now_field(self):
        # H50 sits in `killed` and its `now` reads CONFIRMED. Mark, do not hide.
        e = {'now': 'CONFIRMED, restored the same day by H62'}
        self.assertEqual(bi.superseded_by(e, 'killed'), 'CONFIRMED')

    def test_returns_none_when_bucket_and_now_agree(self):
        self.assertIsNone(bi.superseded_by({'now': 'KILLED on economics'}, 'killed'))

    def test_returns_none_when_there_is_no_now_field(self):
        self.assertIsNone(bi.superseded_by({}, 'killed'))
