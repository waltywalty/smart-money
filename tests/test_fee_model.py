"""C6 - regression tests for analysis/fees/fee_model.py (A1's deliverable).

Run: python3 -m unittest discover -s tests -t .
These lock in the three things A1 established and the two that are still open,
so a future edit cannot quietly reintroduce the whole-cent story.
"""
import math, os, sys, unittest
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'programmes', 'kalshi', 'analysis', 'fees'))
import fee_model as fm


class TestRounding(unittest.TestCase):
    def test_ceil_is_to_a_centicent_not_a_cent(self):
        # The whole point of A1: the trade fee ceiling is $0.0001, not $0.01.
        self.assertEqual(fm.CENTICENT, 0.0001)
        self.assertAlmostEqual(fm._ceil_to(0.00011, fm.CENTICENT), 0.0002, places=9)
        self.assertAlmostEqual(fm._ceil_to(0.0001, fm.CENTICENT), 0.0001, places=9)

    def test_ceil_does_not_round_an_exact_multiple_up(self):
        # Guards the float-error case: ceil(0.0003/0.0001) must not give 4.
        for k in range(1, 200):
            self.assertAlmostEqual(fm._ceil_to(k * fm.CENTICENT, fm.CENTICENT),
                                   k * fm.CENTICENT, places=9)

    def test_floor_to_balance_precision(self):
        self.assertAlmostEqual(fm._floor_to(-1.234, fm.PRECISION_NON_DIRECT), -1.24, places=9)
        self.assertAlmostEqual(fm._floor_to(-1.234, fm.PRECISION_DIRECT), -1.2340, places=9)

    def test_the_two_precisions_are_what_the_docs_say(self):
        self.assertEqual(fm.PRECISION_DIRECT, 0.0001)
        self.assertEqual(fm.PRECISION_NON_DIRECT, 0.01)


class TestDocumentedExamples(unittest.TestCase):
    def test_all_three_worked_examples_reproduce(self):
        # fee_model.test() asserts Kalshi's own three worked examples.
        # If this ever fails, the rounding model has drifted from the docs.
        try:
            fm.test()
        except AssertionError as e:
            self.fail('a documented worked example no longer reproduces: %s' % e)


class TestAccumulator(unittest.TestCase):
    def test_accumulator_is_reported_before_the_rebate(self):
        # This was a real bug: reporting it post-rebate broke all three examples.
        tf, rf, rb, net, bc, acc, shown = fm.fill_fee(-0.055, 0.0085, 0.0, fm.PRECISION_NON_DIRECT)
        self.assertGreaterEqual(shown, acc)

    def test_rebate_only_fires_strictly_above_one_cent(self):
        _, _, rb, _, _, _, _ = fm.fill_fee(-0.01, 0.0, 0.01, fm.PRECISION_NON_DIRECT)
        self.assertEqual(rb, 0.0)

    def test_net_fee_is_never_negative(self):
        for acc in (0.0, 0.005, 0.0099, 0.02, 0.05):
            _, _, _, net, _, _, _ = fm.fill_fee(-0.97, 0.0002, acc, fm.PRECISION_NON_DIRECT)
            self.assertGreaterEqual(net, 0.0)


class TestAmortisation(unittest.TestCase):
    """A1's headline: size matters at the extremes, fragmentation does not."""

    def test_fragmentation_does_not_destroy_amortisation(self):
        a = fm.effective_per_contract(100, 0.97, n_fills=1)
        b = fm.effective_per_contract(100, 0.97, n_fills=5)
        c = fm.effective_per_contract(100, 0.97, n_fills=20)
        self.assertAlmostEqual(a, b, places=4)
        self.assertAlmostEqual(a, c, places=4)

    def test_size_matters_only_at_the_extremes(self):
        # near the middle the ceiling barely binds; at 0.99 it dominates
        mid = fm.effective_per_contract(1, 0.50) / fm.effective_per_contract(100, 0.50)
        ext = fm.effective_per_contract(1, 0.99) / fm.effective_per_contract(100, 0.99)
        self.assertLess(mid, 1.5)
        self.assertGreater(ext, 10.0)

    def test_one_contract_at_an_extreme_costs_a_whole_cent(self):
        # The balance-precision floor for a non-direct member.
        self.assertAlmostEqual(fm.effective_per_contract(1, 0.99), 1.0, places=3)
        self.assertAlmostEqual(fm.effective_per_contract(1, 0.97), 1.0, places=3)

    def test_a_direct_member_does_not_pay_the_one_cent_floor(self):
        direct = fm.effective_per_contract(1, 0.99, target_precision=fm.PRECISION_DIRECT)
        self.assertLess(direct, 1.0)

    def test_inherited_and_documented_COINCIDE_for_a_non_direct_member(self):
        # Measured 2026-08-14, and it is not what P1 assumed. For a non-direct
        # member the balance precision IS one cent, so ceiling the whole order to
        # a cent lands on the same number as the documented per-fill schedule.
        # The INFRA.md formula is wrong in its REASONING, not (here) in its output.
        for contracts, price in ((1, 0.97), (3, 0.50), (100, 0.97), (100, 0.99)):
            with self.subTest(contracts=contracts, price=price):
                doc = fm.effective_per_contract(contracts, price, regime='documented')
                inh = fm.effective_per_contract(contracts, price, regime='inherited')
                self.assertAlmostEqual(doc, inh, places=6)

    def test_the_two_regimes_DO_diverge_for_a_direct_member(self):
        # Where the whole-cent story actually breaks: balance precision 0.0001.
        doc = fm.effective_per_contract(100, 0.97, target_precision=fm.PRECISION_DIRECT,
                                        regime='documented')
        inh = fm.effective_per_contract(100, 0.97, regime='inherited')
        self.assertNotAlmostEqual(doc, inh, places=3)
        self.assertLess(doc, inh)


class TestRateIsAParameter(unittest.TestCase):
    def test_rate_is_not_hardcoded(self):
        # A1 could NOT establish the base rate. It must stay a parameter.
        a = fm.quadratic_base_fee(100, 0.5, rate=0.07)
        b = fm.quadratic_base_fee(100, 0.5, rate=0.035)
        self.assertAlmostEqual(a, 2 * b, places=9)

    def test_multiplier_scales_linearly(self):
        # KXMLBGAME carries fee_multiplier 0.5 - measured 2026-08-14.
        full = fm.quadratic_base_fee(100, 0.6, multiplier=1.0)
        half = fm.quadratic_base_fee(100, 0.6, multiplier=0.5)
        self.assertAlmostEqual(full, 2 * half, places=9)


if __name__ == '__main__':
    unittest.main()
