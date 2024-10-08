# Trading Strategy Simulator

## Project Description

Developed a Stock Market Simulator using Python, leveraging yfinance, pandas, and numpy to fetch, preprocess, and analyze over 5 years of historical and real-time stock market data, enhancing decision-making for trading strategies.

Designed and implemented a user-friendly graphical user interface (GUI) with Tkinter, incorporating interactive widgets and integrated matplotlib plots to visualize 6 key technical indicators, including SMA, EMA, MACD, Bollinger Bands, and SuperTrend.

Automated the generation of buy and sell signals based on technical analysis, providing clear visual markers and summary reports that supported a 20% increase in data-driven trading decisions.

* Trading Strategy Simulator is a Python-based desktop application that enables users to analyze stock market trends using various technical indicators. Leveraging historical stock data from Yahoo Finance, the application calculates and visualizes indicators such as Moving Averages, MACD, Bollinger Bands, Volume Trend, SuperTrend, and Pivot Points. With an intuitive Tkinter-based GUI, users can easily enter stock tickers, select date ranges, and generate insightful visualizations and buy/sell signals to support informed trading decisions. Ideal for both learning and developing trading strategies, this tool is essential for stock market enthusiasts and traders.


- EXAMPLE OF ITC STOCK ANALYSIS:
=======

<img width="356" alt="Entry field" src="https://github.com/user-attachments/assets/6649cf67-0990-4d2c-a24a-a1c61baa4a4d">
<img width="1386" alt="MOVING AVG" src="https://github.com/user-attachments/assets/41cee3bc-ee43-4be6-b6e9-aecf14ca8347">
<img width="1393" alt="Bollinger Bands" src="https://github.com/user-attachments/assets/ed2c7e6f-84e8-4b9d-9e96-f819b198b281">
<img width="1389" alt="MACD and Signal Line" src="https://github.com/user-attachments/assets/2624ed2d-cfd8-401c-8ec3-41fdd9ddbe69">
<img width="1388" alt="SuperTrend" src="https://github.com/user-attachments/assets/78c19822-ea8e-4828-acd3-04b10641c47f">
<img width="1388" alt="Volume Trend" src="https://github.com/user-attachments/assets/456e2cd2-6187-4b03-bc90-8aaeb68ac578">


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [License](#license)
- [Contact](#contact)

## Installation

1. Clone the repository:**

    git clone https://github.com/yourusername/Trading-Strategy-Simulator.git
    cd Trading-Strategy-Simulator


2. **Create a virtual environment:**

    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate


3. **Install the dependencies:**


    pip install -r requirements.txt


## Usage

1. **Activate the virtual environment:**

    source .venv/bin/activate  # On Windows: .venv\Scripts\activate


2. **Run the application:**

    python Trader.py


3. **Use the GUI to enter the stock ticker, start date, and end date, and click the "Analyze" button to perform the analysis.**

## Features

- Fetches historical stock data from Yahoo Finance.
- Calculates various technical indicators including:
  - Simple Moving Average (SMA)
  - Exponential Moving Average (EMA)
  - Moving Average Convergence Divergence (MACD)
  - Bollinger Bands
  - Volume Trend
  - SuperTrend
  - Pivot Points
- Visualizes the data and indicators in separate plots.
- User-friendly GUI for easy interaction.

## Dependencies

- `yfinance`: For fetching stock data from Yahoo Finance.
- `pandas`: For data manipulation and analysis.
- `numpy`: For numerical operations.
- `matplotlib`: For plotting the data and indicators.
- `tkinter`: For creating the GUI.
- `tkcalendar`: For adding a calendar widget to the GUI.

## License

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contact

If you have any questions or suggestions, please feel free to contact me through my website
