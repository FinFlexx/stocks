import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Adjust the display size of the main container
st.markdown(
    """
    <style>
        /* Set width and height of the main container */
        .stApp {
            width: 850px; /* Adjust the width as needed */
            height: 850px; /* Adjust the height as needed */
        }

        /* Hide scrollbar for the whole page */
        body {
            overflow: hidden;
            margin-top: 0;
        }

        header {
            visibility: hidden;
            }
            
        
        /* Remove excess space */
        div[data-testid='stBlock'] div[data-testid='stBlockSpacer'] {
            margin-top: 0;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Sidebar for user input
stocks = {
    'Apple Inc.': 'AAPL',
    'Google': 'GOOGL',
    'Microsoft Corporation': 'MSFT',
    'Tesla Inc.': 'TSLA',
    'Amazon': 'AMZN',
    'Reliance Industries Limited': 'RELIANCE.NS',
    'TCS': 'TCS.NS',
    'Infosys': 'INFY.NS',
    'State Bank of India': 'SBIN.NS',
    'HDFC Bank': 'HDFCBANK.NS',
    # Add more stocks as needed
}

selected_stock = st.sidebar.selectbox("Select Stock", list(stocks.keys()))

time_frames = {
    '2d': '2 Day',
    '5d': '5 Days',
    '1mo': '1 Month',
    '3mo': '3 Months',
    '6mo': '6 Months',
    '1y': '1 Year',
    '5y': '5 Years',
    '10y': '10 Years',
    'max': 'All'
}
selected_time_frame_key = st.sidebar.selectbox(
    "Select Time Frame", list(time_frames.keys()), index=len(time_frames) - 1
)
selected_time_frame = time_frames[selected_time_frame_key]

# Fetch real-time stock data
@st.cache_data
def get_stock_data(symbol, period):
    data = yf.download(symbol, period=period)
    return data

stock_data = get_stock_data(stocks[selected_stock], selected_time_frame_key)


# Plot the stock data
fig = go.Figure()
fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Close'))
fig.update_layout(
    title=f"{selected_stock} Stock Price ({selected_time_frame})",
    xaxis_title="Date",
    yaxis_title="Price",
    width=750,  # Adjust width
    title_font_size=35  # Set title font size
)
st.plotly_chart(fig)

# Print previous closing and opening date and price
previous_close_date = stock_data.index[-2].strftime('%Y-%m-%d')
previous_open_date = stock_data.index[-1].strftime('%Y-%m-%d')
previous_close = round(stock_data['Close'][-2], 4)
previous_open = round(stock_data['Open'][-1], 4)

# Print previous closing and opening date and price with right alignment
st.write(f"<div style='text-align: center;'>Previous Opening Date: {previous_open_date}, Price: {previous_open}</div>", unsafe_allow_html=True)
st.write(f"<div style='text-align: center;'>Previous Closing Date: {previous_close_date}, Price: {previous_close}</div>", unsafe_allow_html=True)


