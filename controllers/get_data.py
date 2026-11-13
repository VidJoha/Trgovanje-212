import csv
import pandas as pd
from pathlib import Path

def get_data(filename,dates,prices):
    BASE_DIR = Path(__file__).resolve().parent.parent
    filename = BASE_DIR/filename
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not row[0][:4].isdigit():
                continue
            dates.append(len(dates))     
            prices.append(float(row[1]))

def get_last_data(ticker_symbol):
    if not ticker_symbol:
        return None
    if isinstance(ticker_symbol, (tuple, list)):
        ticker_symbol = ticker_symbol[0]
    BASE_DIR = Path(__file__).resolve().parent.parent

    output_filename = BASE_DIR/f"{ticker_symbol}_historical_prices.csv"
    df = pd.read_csv(output_filename, skiprows=[1, 2], index_col=0, parse_dates=True)
    latest_price = df["Close"].iloc[-1]
    return latest_price