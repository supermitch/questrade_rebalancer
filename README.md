# questrade_rebalancer

Calculate how to rebalance your portfolio, given your current investment summary.

## Installation

1. Install Python

Then do:

```bash
git clone git@github.com:supermitch/questrade_rebalancer.git
cd questrade_rebalancer
python -m venv venv
source venv/scripts/activate
pip install -U pip
pip install -r requirements.txt
```

## Downloading Investment Summary

1. Log into Questrade
2. Hover over "Reports"
3. Click on "Investment summary"
4. Click "Export to Excel"

## Execution

```bash
cd questrade_rebalancer
source venv/scripts/activate
python qbal.py "~/Downloads/InvestmentSummary.xlsx"
```

## Output

Output will look something like:

```
Total Market Value: $571.09
Class ratio total 0.97600 for symbol XAW.TO is not 100 %
CAD equity:     Target: 25.0 %   Actual: 47.39 % ($270.66)
USA equity:     Target: 25.0 %   Actual: 22.09 % ($126.15)
EAFE equity:    Target: 13.0 %   Actual: 13.05 % ($74.51)
EM equity:      Target: 12.0 %   Actual: 04.80 % ($27.44)
Fixed income:   Target: 25.0 %   Actual: 12.04 % ($68.76)
```
