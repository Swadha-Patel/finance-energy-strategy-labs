import unittest
from model import DEFAULTS, value

class ValuationTests(unittest.TestCase):
    def test_constant_perpetuity(self):
        # 15 annual cash flow at 10% must equal 150 regardless of forecast length.
        a = dict(DEFAULTS, growth=0, terminal_growth=0, da_rate=.03, capex_rate=.03)
        self.assertAlmostEqual(value(a)[1]['enterprise_value'], 150)

    def test_discount_rate_direction(self):
        self.assertLess(value(dict(DEFAULTS, wacc=.12))[1]['enterprise_value'],
                        value(dict(DEFAULTS, wacc=.08))[1]['enterprise_value'])

    def test_equity_bridge(self):
        result = value(DEFAULTS)[1]
        self.assertAlmostEqual(result['enterprise_value']-15, result['equity_value'])

    def test_working_capital_timing(self):
        forecast, _ = value(DEFAULTS)
        self.assertAlmostEqual(forecast[0]['delta_nwc'], 1)
        self.assertAlmostEqual(forecast[0]['fcff'], 13.3)

    def test_invalid_terminal_spread(self):
        with self.assertRaises(ValueError):
            value(dict(DEFAULTS, terminal_growth=.10))

    def test_nan_is_rejected(self):
        with self.assertRaises(ValueError):
            value(dict(DEFAULTS, revenue=float('nan')))

if __name__ == '__main__':
    unittest.main()
