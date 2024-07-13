import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Fetching Data
def fetch_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

# Preprocessing Data
def preprocess_data(stock_data):
    stock_data = stock_data.dropna()
    return stock_data

# Calculating Moving Averages
def calculate_moving_averages(stock_data):
    stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['SMA_200'] = stock_data['Close'].rolling(window=200).mean()
    stock_data['EMA_50'] = stock_data['Close'].ewm(span=50, adjust=False).mean()
    stock_data['EMA_200'] = stock_data['Close'].ewm(span=200, adjust=False).mean()
    return stock_data

# Calculating MACD
def calculate_macd(stock_data):
    stock_data['EMA_12'] = stock_data['Close'].ewm(span=12, adjust=False).mean()
    stock_data['EMA_26'] = stock_data['Close'].ewm(span=26, adjust=False).mean()
    stock_data['MACD'] = stock_data['EMA_12'] - stock_data['EMA_26']
    stock_data['Signal_Line'] = stock_data['MACD'].ewm(span=9, adjust=False).mean()
    return stock_data

# Calculating Bollinger Bands
def calculate_bollinger_bands(stock_data):
    stock_data['20_day_SMA'] = stock_data['Close'].rolling(window=20).mean()
    stock_data['20_day_std'] = stock_data['Close'].rolling(window=20).std()
    stock_data['Upper_Band'] = stock_data['20_day_SMA'] + (stock_data['20_day_std'] * 2)
    stock_data['Lower_Band'] = stock_data['20_day_SMA'] - (stock_data['20_day_std'] * 2)
    return stock_data

# Calculating Volume Trend
def volume_trend(stock_data):
    stock_data['Volume_Trend'] = stock_data['Volume'].rolling(window=20).mean()
    return stock_data

# Calculating SuperTrend
def calculate_supertrend(stock_data, period=7, multiplier=3):
    stock_data['ATR'] = stock_data['High'].rolling(window=period).max() - stock_data['Low'].rolling(window=period).min()
    stock_data['Upper_Band'] = ((stock_data['High'] + stock_data['Low']) / 2) + (multiplier * stock_data['ATR'])
    stock_data['Lower_Band'] = ((stock_data['High'] + stock_data['Low']) / 2) - (multiplier * stock_data['ATR'])
    stock_data['SuperTrend'] = 0.0
    for i in range(1, len(stock_data)):
        if stock_data['Close'][i-1] > stock_data['Upper_Band'][i-1]:
            stock_data['SuperTrend'][i] = stock_data['Upper_Band'][i]
        elif stock_data['Close'][i-1] < stock_data['Lower_Band'][i-1]:
            stock_data['SuperTrend'][i] = stock_data['Lower_Band'][i]
        else:
            stock_data['SuperTrend'][i] = stock_data['SuperTrend'][i-1]
    return stock_data

# Calculating Pivot Points
def calculate_pivot_points(stock_data):
    stock_data['Pivot'] = (stock_data['High'] + stock_data['Low'] + stock_data['Close']) / 3
    stock_data['R1'] = 2 * stock_data['Pivot'] - stock_data['Low']
    stock_data['S1'] = 2 * stock_data['Pivot'] - stock_data['High']
    return stock_data

# Plot Indicators
def plot_indicators(stock_data, ticker):
    plt.figure(figsize=(14, 7))
    plt.plot(stock_data['Close'], label=f'{ticker} Close Price', alpha=0.5)
    plt.plot(stock_data['SMA_50'], label='50-Day SMA', alpha=0.75)
    plt.plot(stock_data['SMA_200'], label='200-Day SMA', alpha=0.75)
    plt.plot(stock_data['EMA_50'], label='50-Day EMA', alpha=0.75)
    plt.plot(stock_data['EMA_200'], label='200-Day EMA', alpha=0.75)
    plt.title(f'{ticker} Stock Price with Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Close Price (INR)')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(14, 7))
    plt.plot(stock_data['Close'], label=f'{ticker} Close Price', alpha=0.5)
    plt.plot(stock_data['Upper_Band'], label='Upper Bollinger Band', alpha=0.75)
    plt.plot(stock_data['Lower_Band'], label='Lower Bollinger Band', alpha=0.75)
    plt.fill_between(stock_data.index, stock_data['Lower_Band'], stock_data['Upper_Band'], alpha=0.1)
    plt.title(f'{ticker} Stock Price with Bollinger Bands')
    plt.xlabel('Date')
    plt.ylabel('Close Price (INR)')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(14, 7))
    plt.plot(stock_data['MACD'], label='MACD', alpha=0.75)
    plt.plot(stock_data['Signal_Line'], label='Signal Line', alpha=0.75)
    plt.title(f'{ticker} MACD and Signal Line')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(14, 7))
    plt.plot(stock_data['Volume_Trend'], label='20-Day Volume Trend', alpha=0.75)
    plt.title(f'{ticker} Volume Trend')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(14, 7))
    plt.plot(stock_data['Close'], label=f'{ticker} Close Price', alpha=0.5)
    plt.plot(stock_data['SuperTrend'], label='SuperTrend', alpha=0.75)
    plt.title(f'{ticker} SuperTrend')
    plt.xlabel('Date')
    plt.ylabel('Close Price (INR)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Calculating Buy/Sell Signals based on Trading Strategy
def trading_strategy(stock_data):
    stock_data['Buy_Signal'] = np.where((stock_data['Close'] > stock_data['SuperTrend']) & (stock_data['Close'] > stock_data['R1']), stock_data['Close'], np.nan)
    stock_data['Sell_Signal'] = np.where((stock_data['Close'] < stock_data['SuperTrend']), stock_data['Close'], np.nan)
    return stock_data

# Function to execute analysis and display plots
def execute_analysis():
    ticker = ticker_entry.get()
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()

    stock_data = fetch_data(ticker, start_date, end_date)
    stock_data = preprocess_data(stock_data)
    stock_data = calculate_moving_averages(stock_data)
    stock_data = calculate_macd(stock_data)
    stock_data = calculate_bollinger_bands(stock_data)
    stock_data = volume_trend(stock_data)
    stock_data = calculate_supertrend(stock_data)
    stock_data = calculate_pivot_points(stock_data)
    stock_data = trading_strategy(stock_data)

    plot_indicators(stock_data, ticker)


root = tk.Tk()
root.title("Stock Market Analysis")


style = ttk.Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12))

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(main_frame, text="Stock(NIFTY FIFTY):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
ticker_entry = ttk.Entry(main_frame, width=20)
ticker_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

ttk.Label(main_frame, text="Start Date:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
start_date_entry = DateEntry(main_frame, width=18, background='white', foreground='white', borderwidth=2, year=2023, date_pattern='y-mm-dd')
start_date_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

ttk.Label(main_frame, text="End Date:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
end_date_entry = DateEntry(main_frame, width=18, background='white', foreground='white', borderwidth=2, year=2023, date_pattern='y-mm-dd')
end_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

analyze_button = ttk.Button(main_frame, text="Analyze", command=execute_analysis)
analyze_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

root.mainloop()
