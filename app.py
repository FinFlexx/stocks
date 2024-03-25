import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

st.set_option('deprecation.showPyplotGlobalUse', False)


def main():
    
    
    # Fetch historical market data
    ticker_symbol = 'AAPL'  # Apple Inc.
    start_date = datetime(1999, 1, 1)
    end_date = datetime(2024, 3, 24)
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)

    # Plotting the closing price of the stock
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data['Close'])
    plt.title(f'Stock Price of {ticker_symbol}')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (USD)')
    plt.grid(True)

    # Display the plot in Streamlit
    st.pyplot()

if __name__ == "__main__":
    main()


