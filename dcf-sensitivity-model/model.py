"""Dependency-free educational FCFF valuation. All inputs are illustrative."""
import argparse
import csv
import json
import math
from pathlib import Path

DEFAULTS = dict(revenue=100.0, growth=.10, margin=.20, tax=.25, da_rate=.03,
                capex_rate=.05, nwc_rate=.10, years=5, wacc=.10,
                terminal_growth=.025, terminal_roic=.15, cash=15.0, debt=30.0,
                shares=10.0)


def validate(a):
    if any(not math.isfinite(v) for v in a.values()):
        raise ValueError('All assumptions must be finite numbers')
    if a['years'] < 1 or int(a['years']) != a['years']:
        raise ValueError('years must be a positive integer')
    if min(a['revenue'], a['shares'], a['terminal_roic']) <= 0:
        raise ValueError('revenue, shares and terminal_roic must be positive')
    if not 0 <= a['terminal_growth'] < min(a['wacc'], a['terminal_roic']):
        raise ValueError('Require 0 <= terminal_growth < WACC and terminal ROIC')
    if a['growth'] <= -1:
        raise ValueError('growth must exceed -100%')
    for key in ['margin', 'tax', 'da_rate', 'capex_rate', 'nwc_rate']:
        if not 0 <= a[key] <= 1:
            raise ValueError(f'{key} must be between 0 and 1')
    if min(a['cash'], a['debt']) < 0:
        raise ValueError('cash and debt cannot be negative')


def value(a):
    validate(a)
    revenue = a['revenue']
    rows = []
    for year in range(1, int(a['years']) + 1):
        prior = revenue
        revenue *= 1 + a['growth']
        nopat = revenue * a['margin'] * (1-a['tax'])
        da, capex = revenue*a['da_rate'], revenue*a['capex_rate']
        delta_nwc = (revenue-prior)*a['nwc_rate']
        fcff = nopat + da-capex-delta_nwc
        rows.append(dict(year=year, revenue=revenue, nopat=nopat, da=da,
                         capex=capex, delta_nwc=delta_nwc, fcff=fcff,
                         pv_fcff=fcff/(1+a['wacc'])**year))
    # Normalize reinvestment in perpetuity: growth / return on invested capital.
    terminal_nopat = rows[-1]['nopat']*(1+a['terminal_growth'])
    terminal_fcff = terminal_nopat*(1-a['terminal_growth']/a['terminal_roic'])
    terminal_value = terminal_fcff/(a['wacc']-a['terminal_growth'])
    pv_terminal = terminal_value/(1+a['wacc'])**a['years']
    ev = sum(r['pv_fcff'] for r in rows) + pv_terminal
    equity = ev+a['cash']-a['debt']
    summary = dict(enterprise_value=ev, equity_value=equity,
                   value_per_share=equity/a['shares'], terminal_fcff=terminal_fcff,
                   terminal_value=terminal_value, pv_terminal=pv_terminal,
                   terminal_share_of_ev=pv_terminal/ev if ev else None)
    return rows, summary


def write_csv(path, rows):
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path('results'))
    parser.add_argument('--wacc', type=float, default=DEFAULTS['wacc'])
    parser.add_argument('--growth', type=float, default=DEFAULTS['growth'])
    parser.add_argument('--terminal-growth', type=float, default=DEFAULTS['terminal_growth'])
    args = parser.parse_args()
    assumptions = dict(DEFAULTS, wacc=args.wacc, growth=args.growth,
                       terminal_growth=args.terminal_growth)
    try:
        forecast, summary = value(assumptions)
        matrix = []
        for wacc in [.08, .09, .10, .11, .12]:
            row = {'wacc': wacc}
            for g in [.015, .020, .025, .030, .035]:
                row[f'g_{g:.3f}'] = value(dict(assumptions, wacc=wacc, terminal_growth=g))[1]['value_per_share']
            matrix.append(row)
    except ValueError as error:
        parser.error(str(error))
    args.out.mkdir(parents=True, exist_ok=True)
    write_csv(args.out/'forecast.csv', forecast)
    write_csv(args.out/'sensitivity.csv', matrix)
    write_csv(args.out/'valuation.csv', [summary])
    (args.out/'assumptions.json').write_text(json.dumps(assumptions, indent=2)+'\n')
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
