# app.py
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go


# Set page configuration
st.set_page_config(menu_items={ "About": None, })


# Adjust the display size of the main container
st.markdown("""
    <style>
        /* Set width and height of the main container */
        .stApp {
            width: 800px; /* Adjust the width as needed */
            height: 800px; /* Adjust the height as needed */
        }

        /* Hide scrollbar for the whole page */
        body {
            overflow: hidden;
            margin-top: 0;
        }
        
        /* Remove excess space */
        div[data-testid='stBlock'] div[data-testid='stBlockSpacer'] {
            margin-top: 0;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar for user input
time_frames = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '5y', '10y', 'max']
selected_time_frame = st.sidebar.selectbox("Select Time Frame", time_frames, index=len(time_frames)-1)

# Fetch real-time stock data
@st.cache_data
def get_stock_data(symbol, period):
    data = yf.download(symbol, period=period)
    return data

stock_data = get_stock_data('RELIANCE.NS', selected_time_frame)

# Plot the stock data
fig = go.Figure()
fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Close'))
fig.update_layout(title='RELIANCE Stock Price', xaxis_title='Date', yaxis_title='Price')
st.plotly_chart(fig)
