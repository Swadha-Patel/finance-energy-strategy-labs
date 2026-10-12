"""Synthetic SaaS cohort economics; no dependencies or external data."""
import argparse
import csv
import json
import math
from pathlib import Path

SCENARIOS = {
    'efficient': dict(customers=100, cac=700, arpa=110, margin=.82, churn=.015),
    'base': dict(customers=100, cac=900, arpa=100, margin=.80, churn=.025),
    'stressed': dict(customers=100, cac=1400, arpa=90, margin=.72, churn=.05),
}


def cohort(a, months=36):
    if any(not math.isfinite(v) for v in a.values()):
        raise ValueError('All inputs must be finite')
    if months < 1 or int(months) != months:
        raise ValueError('months must be a positive integer')
    if a['customers'] <= 0 or a['cac'] < 0 or a['arpa'] <= 0:
        raise ValueError('customers and ARPA must be positive; CAC cannot be negative')
    if not 0 <= a['churn'] <= 1 or not 0 < a['margin'] <= 1:
        raise ValueError('Require churn in [0,1] and gross margin in (0,1]')
    initial_spend = a['customers']*a['cac']
    active = a['customers']
    cumulative = 0.0
    payback_month = 0 if initial_spend == 0 else None
    rows = []
    for month in range(1, months+1):
        # Customers pay for the current month; churn occurs at month-end.
        revenue = active*a['arpa']
        gross_profit = revenue*a['margin']
        cumulative += gross_profit
        if payback_month is None and cumulative >= initial_spend:
            payback_month = month
        rows.append(dict(month=month, expected_active_customers=active,
                         revenue=revenue, gross_profit=gross_profit,
                         cumulative_gross_profit=cumulative,
                         unrecovered_cac=max(0, initial_spend-cumulative),
                         cumulative_contribution=cumulative-initial_spend))
        active *= 1-a['churn']
    monthly_gp = a['arpa']*a['margin']
    lifetime_gp = monthly_gp/a['churn'] if a['churn'] else None
    summary = dict(initial_acquisition_spend=initial_spend,
                   static_payback_months=a['cac']/monthly_gp,
                   cohort_payback_month=payback_month,
                   horizon_months=months,
                   horizon_contribution=cumulative-initial_spend,
                   infinite_horizon_gp_per_customer=lifetime_gp,
                   gp_ltv_to_cac=lifetime_gp/a['cac'] if lifetime_gp is not None and a['cac'] else None,
                   max_cac_for_horizon_payback=cumulative/a['customers'])
    return rows, summary


def write_csv(path, rows):
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--months', type=int, default=36)
    parser.add_argument('--out', type=Path, default=Path('results'))
    parser.add_argument('--cac-multiplier', type=float, default=1)
    args = parser.parse_args()
    assumptions = {name: dict(a, cac=a['cac']*args.cac_multiplier) for name, a in SCENARIOS.items()}
    summaries, detailed = [], {}
    try:
        if not math.isfinite(args.cac_multiplier) or args.cac_multiplier < 0:
            raise ValueError('CAC multiplier must be finite and nonnegative')
        for name, a in assumptions.items():
            rows, summary = cohort(a, args.months)
            detailed[name] = rows
            summaries.append(dict(scenario=name, **summary))
    except ValueError as error:
        parser.error(str(error))
    args.out.mkdir(parents=True, exist_ok=True)
    for name, rows in detailed.items():
        write_csv(args.out/f'{name}_cohort.csv', rows)
    write_csv(args.out/'scenario_comparison.csv', summaries)
    (args.out/'assumptions.json').write_text(json.dumps(assumptions, indent=2)+'\n')
    print(json.dumps(summaries, indent=2))

if __name__ == '__main__':
    main()
