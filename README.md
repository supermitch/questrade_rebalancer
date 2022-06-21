# questrade_rebalancer

Calculate how to rebalance your portfolio, given your current investment summary.

## Installation

1. Install Python

Then do:

```bash
git clone git@github.com:supermitch/questrade_rebalancer.git
cd questrade_reblancer
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
cd questrade_reblancer
source venv/scripts/activate
python qbal.py "~/Downloads/InvestmentSummary.xlsx"
```
