# Finance & Energy Strategy Labs

Three independent educational projects exploring business decisions with transparent models. All inputs are illustrative, not real client outcomes, investment recommendations, or vendor quotes.

| Project | Question | Runtime |
|---|---|---|
| [DCF sensitivity](dcf-sensitivity-model/) | How do growth and discount rates change value? | Python 3 |
| [GTM unit economics](gtm-unit-economics/) | When does a customer cohort recover acquisition cost? | Python 3 |
| [Energy capital allocation](energy-capital-allocation/) | Which efficiency, solar or storage scenario creates value? | Node.js |

No third-party packages are required. Each folder includes source, documentation and tests; the Python projects include generated CSV examples.

## Run & test

```sh
cd dcf-sensitivity-model
python3 model.py
python3 -m unittest
cd ../gtm-unit-economics
python3 model.py
python3 -m unittest
cd ../energy-capital-allocation
node run.js
node test.js
```

## Interpretation

The purpose is to expose trade-offs and sensitivity, not to force an attractive answer. Forecasts are conditional on assumptions. Energy alternatives may have negative NPV; unit economics may never pay back within the modeled horizon. Read each project's limitations before interpreting outputs.

[Portfolio](https://swadha-patel-strategy.fungrape1.chatgpt.site) — interactive versions are available on the owner's private review site.
