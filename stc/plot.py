import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
from matplotlib.animation import FuncAnimation
import pandas as pd

# Get live stock data from yfinance
""" def fetch_stock_data(ticker, period="1d", interval="1m"):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period, interval=interval)
    return data

# Function to plot line chart
def plot_line(ax, data):
    ax.clear()
    ax.plot(data.index, data['Close'], color='blue', label='Close Price')
    ax.set_title('Line Chart - Close Price')
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

# Function to plot bar chart
def plot_bar(ax, data):
    ax.clear()
    ax.bar(data.index, data['Volume'], color='orange', label='Volume')
    ax.set_title('Bar Chart - Volume')
    ax.set_xlabel('Time')
    ax.set_ylabel('Volume')
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

# Function to plot candlestick chart
def plot_candlestick(ax, data):
    ax.clear()
    mpf.plot(data, type='candle', ax=ax, style='charles', show_nontrading=True)
    ax.set_title('Candlestick Chart')
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')

# Animation function to update the graphs
def animate(i, ticker, ax_line, ax_bar, ax_candle):
    data = fetch_stock_data(ticker)
    if not data.empty:
        plot_line(ax_line, data)
        plot_bar(ax_bar, data)
        plot_candlestick(ax_candle, data)

# Main function to setup the live graphs
def live_stock_plot(ticker):
    fig, (ax_line, ax_bar, ax_candle) = plt.subplots(3, 1, figsize=(12, 15))
    plt.suptitle(f'Live Stock Data for {ticker}', fontsize=16)

    # Adjust the layout to add more space between subplots
    plt.subplots_adjust(hspace=0.5)

    ani = FuncAnimation(fig, animate, fargs=(ticker, ax_line, ax_bar, ax_candle), interval=60000)  # Update every 60 seconds
    plt.show()

# Get the stock ticker symbol from the user
ticker = input("Enter the stock ticker symbol (e.g., AAPL, TSLA): ").upper()
live_stock_plot(ticker)
 """


stock = yf.Ticker("TCS.NS")
current_price = stock.fast_info.last_price
print(current_price)