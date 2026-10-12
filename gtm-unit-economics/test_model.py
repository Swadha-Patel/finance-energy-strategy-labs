import unittest
from model import SCENARIOS, cohort

class CohortTests(unittest.TestCase):
    def test_zero_churn_recovery(self):
        a = dict(SCENARIOS['base'], cac=160, arpa=100, margin=.8, churn=0)
        rows, summary = cohort(a, 3)
        self.assertEqual(summary['cohort_payback_month'], 2)
        self.assertEqual(rows[-1]['expected_active_customers'], 100)
        self.assertEqual(summary['horizon_contribution'], 8000)

    def test_churn_changes_recovery(self):
        a = dict(SCENARIOS['base'], cac=160, arpa=100, margin=.8, churn=.5)
        _, summary = cohort(a, 36)
        self.assertIsNone(summary['cohort_payback_month'])
        self.assertEqual(summary['static_payback_months'], 2)

    def test_full_churn_one_month_revenue(self):
        rows, summary = cohort(dict(SCENARIOS['base'], churn=1), 3)
        self.assertEqual(rows[1]['revenue'], 0)
        self.assertEqual(summary['infinite_horizon_gp_per_customer'], 80)

    def test_zero_cac_immediate_payback(self):
        _, summary = cohort(dict(SCENARIOS['base'], cac=0))
        self.assertEqual(summary['cohort_payback_month'], 0)
        self.assertIsNone(summary['gp_ltv_to_cac'])

    def test_geometric_sum(self):
        a = SCENARIOS['base']
        rows, _ = cohort(a, 12)
        expected = a['customers']*a['arpa']*a['margin']*(1-(1-a['churn'])**12)/a['churn']
        self.assertAlmostEqual(rows[-1]['cumulative_gross_profit'], expected)

    def test_invalid_churn(self):
        with self.assertRaises(ValueError):
            cohort(dict(SCENARIOS['base'], churn=1.1))

if __name__ == '__main__':
    unittest.main()
