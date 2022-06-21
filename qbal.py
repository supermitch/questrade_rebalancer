#!/usr/bin/env python
import argparse
import math
import pathlib
import warnings
from collections import defaultdict
from pprint import pprint

import openpyxl

# Symbols
VAB = 'VAB.TO'
VCN = 'VCN.TO'
VEE = 'VEE.TO'
VEQT = 'VEQT.TO'
VIU = 'VIU.TO'
XAW = 'XAW.TO'
ZAG = 'ZAG.TO'

# Asset class
CAD_EQUITY = 'CAD equity'
US_EQUITY = 'USA equity'
EM_EQUITY = 'EM equity'
EAFE_EQUITY = 'EAFE equity'
FIXED_INCOME = 'Fixed income'

symbol_classes = {
    VAB: {FIXED_INCOME: 1.0},
    VCN: {CAD_EQUITY: 1.0},
    VEE: {EM_EQUITY: 1.0},
    VEQT: {
        US_EQUITY: 0.4199,
        CAD_EQUITY: 0.3001,
        EAFE_EQUITY: 0.2013,
        EM_EQUITY: 0.0787,
    },
    VIU: {EAFE_EQUITY: 1.0},
    XAW: {
        US_EQUITY: (0.5136 + 0.0358 + 0.0266),
        EAFE_EQUITY: 0.2728,
        EM_EQUITY: 0.1272,
    },
    ZAG: {FIXED_INCOME: 1.0},
}

target_allocations = {
    CAD_EQUITY: 0.25,
    US_EQUITY: 0.25,
    EM_EQUITY: 0.12,
    EAFE_EQUITY: 0.13,
    FIXED_INCOME: 0.25,
}

class COLS:
    equity_symbol = 'Equity Symbol'
    equity_desc = 'Equity Description'
    account_number = 'Account Number'
    currency = 'Currency'
    cost_basis = 'Cost Basis'
    asset_class = 'Asset Class'
    quantity = 'Quantity'
    cost_per_share = 'Cost Per Share'
    position_cost = 'Position Cost'
    market_price = 'Market Price'
    market_value = 'Market Value'
    profit_and_loss = 'Profit And Loss'
    percent_return = '% Return'
    percent_of_portfolio = '% of Portfolio'


def parse_args():
    parser = argparse.ArgumentParser(description='Questrade Rebalancer')
    parser.add_argument('summary', help='Path to investment summary .xlsx')
    return parser.parse_args()


def read_workbook(in_path):
    """
    Read an Investment Summary workbook into a dict of columns (keyed by header)
    and a list of rows, each row is a dict keyed by header.
    """
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')  # Suppress openpyxl stylesheet warning
        wb = openpyxl.load_workbook(filename=str(in_path))
    ws = wb['Positions']
    data = list(ws.values)  # type: ignore
    headers = data[0]
    raw_rows = data[1:]

    cols = defaultdict(list)
    for row in raw_rows:
        for header, value in zip(headers, row):
            cols[header].append(value)

    rows = []
    for row in raw_rows:
        rows.append({k: v for k, v in zip(headers, row)})

    return rows, cols


def main():
    args = parse_args()
    summary_path = pathlib.Path(args.summary).expanduser()
    if not summary_path.is_file():
        raise FileNotFoundError('Summary .xlsx path not found')
    rows, cols = read_workbook(summary_path)

    total_mkt_val = sum(cols[COLS.market_value])
    print(f'Total Market Value: ${total_mkt_val:,.2f}')

    val_by_symb = defaultdict(int)
    for row in rows:
        val_by_symb[row[COLS.equity_symbol]] += row[COLS.market_value]

    val_by_class = defaultdict(float)
    for symbol, mkt_value in val_by_symb.items():
        class_ratios = symbol_classes[symbol]
        ratio_sum = 0
        for class_, ratio in class_ratios.items():
            ratio_sum += ratio
            val_by_class[class_] += ratio * mkt_value
        if not math.isclose(ratio_sum, 1.0, abs_tol=1e-3):
            print(f'Class ratio total {ratio_sum:.5f} for symbol {symbol} is not 100 %')

    for class_, mkt_value in val_by_class.items():
        percent_of_port = mkt_value / total_mkt_val * 100

        print(
            f'{class_ + ":": <15}'
            f' Target: {target_allocations[class_] * 100:03.1f} %  '
            f' Actual: {percent_of_port:05.2f} % (${mkt_value:,.2f})'
        )


if __name__ == '__main__':
    main()
