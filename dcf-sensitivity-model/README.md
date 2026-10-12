# DCF Sensitivity Lab

A new educational portfolio project: a transparent, dependency-free valuation model for a fictional operating business. It is not an estimate of a real company's value or a historical client engagement. Use it to explore how operating growth, reinvestment and the cost of capital change a valuation.

## Run

Requires Python 3.9+; no installation or third-party libraries.

```sh
python3 model.py
python3 model.py --wacc 0.11 --growth 0.08 --terminal-growth 0.02 --out custom-results
python3 -m unittest -v
```

Rates use decimal notation. Output files are written relative to your current directory. The committed `results/` files are an executed example with the defaults.

## Illustrative inputs

All company amounts are USD millions; shares are millions, giving USD per share. Starting revenue 100, annual revenue growth 10%, EBIT margin 20%, tax 25%, depreciation 3% of revenue, capex 5%, noncash working capital 10%, five forecast years, WACC 10%, perpetual growth 2.5%, terminal ROIC 15%, cash 15, debt 30 and shares 10. These inputs are synthetic assumptions, not researched market estimates.

## Model

Revenue grows annually. NOPAT = revenue × EBIT margin × (1 − tax). FCFF = NOPAT + depreciation − capex − change in noncash working capital. Working capital starts at 10% of starting revenue; each year's change uses incremental revenue. Cash flows occur at year-end and are discounted at WACC.

For the terminal phase, next-year NOPAT grows at the perpetual growth rate. Terminal reinvestment = growth / terminal ROIC; terminal FCFF = next-year NOPAT × (1 − reinvestment). This explicitly funds perpetual growth rather than simply growing the last forecast cash flow. Terminal value = terminal FCFF / (WACC − growth), discounted back five years. Enterprise value is forecast PV plus terminal PV. Equity value adds cash and subtracts debt; per-share value divides by shares.

## Outputs and strategic use

- `forecast.csv`: operating forecast and annual discounted FCFF.
- `valuation.csv`: enterprise/equity values and terminal-value concentration.
- `sensitivity.csv`: per-share valuation across five WACCs and five terminal growth assumptions. This fixed grid is a comparison reference; CLI changes affect the operating forecast, while grid WACC/g override the corresponding CLI values.
- `assumptions.json`: exact base-case parameters for reproducibility.

The terminal share of enterprise value indicates how much of the answer depends on distant expectations. Compare the valuation range with the value of operational initiatives before discussing a transaction or capital allocation. A lower discount rate is an assumption, not an operational achievement. Higher growth consumes reinvestment; the model makes that tradeoff visible.

## Limits and extensions

Constant margins and annual growth simplify business cycles. Tax loss carryforwards, dilution, leases, pensions, excess assets, probability-weighted cases and midyear discounting are excluded. Terminal operating economics switch immediately to the normalized ROIC assumption. This model targets profitable operating companies and does not model banks, distress or negative-margin firms. Add company filings, a year-by-year operating plan and independent assumption review before using it for a real decision. No investment recommendation is made.

Formula reference: [Aswath Damodaran, NYU Stern — estimating terminal value](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/valquestions/termvalapproaches.htm), and [stable reinvestment guidance](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/project/prques.htm).

## GitHub-ready

This folder can be published as its own repository. Review the assumptions and README, then initialize Git and push using your own authenticated GitHub account. No remote repository has been created by this project.
