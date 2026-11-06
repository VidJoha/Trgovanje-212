import matplotlib.pyplot as plt
from controllers.get_data import get_data
import sqlite3
from datetime import date, timedelta
import yfinance as yf

def plotaj(ime):
    connection = sqlite3.connect('dionice.db')
    cursor=connection.cursor()

    cursor.execute("SELECT TICKER FROM DIONICE WHERE DIONICE.IME_DIONICE=?",(ime,))
    ticker_symbol = cursor.fetchone()[0]

    dates=[]
    prices=[]
    start_date = "2026-01-01"
    end_date = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")

    df = yf.download(ticker_symbol, start=start_date, end=end_date)
    output_filename = f"{ticker_symbol}_historical_prices.csv"
    df.to_csv(output_filename)
    get_data(output_filename,dates,prices)

    plt.plot(dates,prices, c = "green", label = ime)
    plt.xlabel("Vrijeme")
    plt.ylabel("Cijena dionice")
    plt.title(f"Cijena dionice {ime}")
    plt.show()