# Go-to-Market Economics Lab

A new educational portfolio project that compares SaaS acquisition efficiency, retention and cohort payback. All customers, prices and scenarios are synthetic. This is an independent analysis tool, not a past employer project or evidence of achieved commercial outcomes.

## Run

Python 3.9+ and its standard library are sufficient.

```sh
python3 model.py
python3 model.py --months 24 --cac-multiplier 1.2 --out custom-results
python3 -m unittest -v
```

Default CSV results are committed in `results/`. Each run writes three monthly cohort CSVs, a scenario comparison and the exact assumptions. A blank payback cell means acquisition cost was not recovered within the selected horizon; it does not always mean it will never be recovered.

## Illustrative scenarios

| Scenario | Initial customers | CAC ($) | Monthly ARPA ($) | Gross margin | Monthly churn |
|---|---:|---:|---:|---:|---:|
| Efficient | 100 | 700 | 110 | 82% | 1.5% |
| Base | 100 | 900 | 100 | 80% | 2.5% |
| Stressed | 100 | 1,400 | 90 | 72% | 5.0% |

These are deliberately contrasting assumptions, not industry benchmarks. CAC is assumed fully loaded and paid at cohort acquisition. ARPA means average monthly revenue per account; churn is customer churn. Currency is USD throughout.

## Formulas and timing

A cohort is acquired at month zero. Expected customers in month t = initial customers × (1 − churn)^(t − 1). Customers generate revenue before month-end churn. Fractional customer counts are expectations. Monthly revenue = expected customers × ARPA; gross profit = revenue × gross margin. Cumulative contribution = cumulative gross profit − initial acquisition spend.

Static payback = CAC / (ARPA × gross margin). Cohort payback is the first whole month cumulative gross profit covers acquisition spend, so it includes the effect of churn. With zero CAC, payback is month zero. The model also reports the maximum CAC recoverable over the selected horizon.

Undiscounted infinite-horizon gross-profit LTV = ARPA × gross margin / churn for positive constant churn. Zero churn produces no finite LTV, so the field is blank/null. A zero CAC makes the LTV/CAC ratio undefined and it is also blank/null. These fields are not discounted company valuations.

## Strategic interpretation

Compare static payback with cohort payback before scaling an acquisition channel. The gap exposes the cost of attrition. The stressed case can have attractive initial revenue while failing to recover acquisition costs: retention and gross margin matter as much as conversion volume. Compare maximum recoverable CAC with channel bids to form a spending ceiling under an explicit horizon. Sensitivity is a decision aid, not proof that the efficient scenario can be achieved.

## Limits and next work

One cohort; constant churn, prices and margins; no expansion, reactivation, onboarding lag, fixed overhead, taxes, financing costs or cash collection delay. Gross profit less CAC is not net income or full operating cash flow. Infinite-horizon LTV can be optimistic and is not risk-adjusted. Replace inputs with reconciled CRM/billing data and add retention curves and channel cohorts before operational use.

Formula reference: [Stripe — CAC payback period](https://stripe.com/resources/more/what-is-the-cac-payback-period). The churn-adjusted cohort simulation is explicitly documented above and tested against the geometric-series sum.

## GitHub-ready

Publish this directory as its own repository after reviewing it. No remote GitHub repository has been created. The code has no credentials, external data requirements or dependencies.
