# Houston Energy Capital Lab

An educational capital-allocation project for a fictional Houston commercial business. Compare grid-only (incremental NPV = $0), rooftop solar, and rooftop solar + storage. All inputs below are synthetic assumptions, NOT an actual Houston tariff, vendor quote, measured customer load, historical client result or tax advice. Explain this directly beside the controls. Provide a clickable browser workspace instead of requiring a download.

## Recommended simple, auditable version

Use a 15-year nominal, unlevered, pre-tax cash-flow model. Set tax incentives, financing, residual value, insurance, grid export revenue, resilience value and demand-charge savings to zero. This avoids making unsupported eligibility or tariff assumptions. Hold prices and O&M constant (0% escalation). State that omissions can materially change real project economics.

Default solar system: 100 kW; installed cost $2,000/kW; first-year yield 1,450 kWh/kW; direct daytime self-consumption 65%; degradation 0.5%/year; solar O&M 1% of original solar capex/year.
Default battery: 100 kWh usable energy; capex $500/kWh; round-trip efficiency 90%; annual throughput ceiling 250 full charging cycles; battery O&M 1.5% of battery capex/year. Assume 2% annual decline in usable energy, battery replacement at end of year 10 costing 70% of original battery capex; replaced unit resets capacity in year 11. This replacement cost is synthetic, not a prediction.
Default avoided retail energy price $0.14/kWh; discount rate 8%. Battery charges only from the solar portion not directly consumed; no grid arbitrage. Assume sufficient evening site demand to absorb discharged energy; cannot claim this is guaranteed for a real business.

For year t = 1..15:
- Generation G_t = solarKW × annualYield × (1 − 0.005)^(t−1).
- Direct use D_t = G_t × selfConsumption.
- Excess X_t = G_t − D_t.
- Battery age = t−1 for t<=10, else t−11.
- Battery charging energy Q_t = min(X_t, batteryKWh × 250 × 0.98^age).
- Battery delivered energy B_t = Q_t × 0.90.
- Solar cash flow = D_t × energyPrice − solarCapex × 0.01.
- Solar + storage cash flow = (D_t + B_t) × energyPrice − solarCapex × 0.01 − batteryCapex × 0.015 − (t==10 ? batteryCapex × 0.70 : 0).
- Initial solar investment = solarKW × costPerKW.
- Initial combined investment = solarCapex + batteryCapex.
- NPV = −initialInvestment + sum(CF_t / (1 + discountRate)^t).
- First-year energy savings = avoided purchased kWh × energyPrice (gross, before O&M).
- Annual operating benefit = gross energy savings − annual O&M (distinct from gross savings).
- Discounted payback: first year cumulative discounted cash flow >=0; if none, display “Beyond 15 years”. Label this “First discounted break-even” if later replacement can push cumulative cash negative again; preferably calculate sustained break-even after which all future cumulative amounts remain >=0.

Useful controls: avoided energy price $0.06–$0.30/kWh; solar cost $1,000–$3,000/kW; direct self-consumption 30%–95%; discount rate 3%–15%; storage on/off. Recompute all years. Show solar-only NPV, combined NPV, incremental battery NPV (combined−solar), and first-year avoided grid kWh. Default may favor grid-only; do not tune assumptions just to claim a positive renewable project. A negative battery NPV is a legitimate strategy insight under a flat energy tariff and zero resilience/demand-charge value.

Interpretation: “At these assumptions, [option] has the highest modeled incremental NPV. Before making a real decision, add interval load data, a vendor design and the actual retail contract.” Avoid calling modeled avoided grid energy an emissions reduction: no grid emissions factor or dispatch analysis is included.

## Build data transparency into the page

Include a readable assumption table, model limitations, a 15-row cash-flow table, and “How it works” formulas. Do not add a generic decorative graph above every project. Optional within this specific calculator: a small cumulative cash-flow chart only if it improves comprehension.

## Recent context (not model calibration)

- EIA, August 7, 2026: https://www.eia.gov/todayinenergy/detail.php?id=67925
- ERCOT June 1–2, 2026 CEO update: https://www.ercot.com/files/docs/2026/05/28/11-CEO-Update.pdf

The linked articles motivate the strategy question. None of their utility-scale figures are being used as a commercial rooftop cost or return estimate.

## Run the implemented project

Requires Node.js. No packages required.

```sh
node run.js
node run.js 0.20
node test.js
```

The optional CLI argument is the avoided energy price in USD/kWh. Output includes the complete 15-year cash-flow schedule and NPVs.

The implemented version also compares a separate efficiency project: $30,000 initial cost, 500,000 kWh annual baseline demand, 12% demand reduction, and $300 annual O&M. These are synthetic inputs. Efficiency cash flow = 500,000 × 12% × energy price − 300; NPV uses the same 15-year horizon and discount rate. It is an alternative, not stacked on top of solar.

`models.js` shares the calculation engine with the portfolio and also exports the DCF and GTM functions. [Explore the live lab](https://swadha-patel-strategy.fungrape1.chatgpt.site/#project/energy); the portfolio currently requires its owner's access.
