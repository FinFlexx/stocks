import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
# import yfinance as yf
from yahoo_fin.stock_info import get_data
from streamlit_option_menu import option_menu
import warnings
warnings.filterwarnings('ignore')
import sklearn.metrics as metrics

# Set the layout as wide
st.set_page_config(layout="wide")

def get_stock_data(ticker):
    df = get_data(ticker, start_date = None, end_date = None, index_as_date = False, interval ='1d')
    return df

def main():
    st.title("Predictor")
    ticker = st.selectbox("Pick any stock or index to predict:" ,
        ('AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'SBIN.NS', 'HDFCBANK.NS'))

    
    if st.button('Predict'):
        df = get_stock_data(ticker)
        ## ------------------------------- PREDICTION LOGIC -------------------------------
        # Data Cleaning
        mean = df['open'].mean()
        df['open'] = df['open'].fillna(mean)

        mean = df['high'].mean()
        df['high'] = df['high'].fillna(mean)

        mean = df['low'].mean()
        df['low'] = df['low'].fillna(mean)

        mean = df['close'].mean()
        df['close'] = df['close'].fillna(mean)

        X = df[['open','high','low']]
        y = df['close'].values.reshape(-1,1)
        
        #Splitting our dataset to Training and Testing dataset
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        #Fitting Linear Regression to the training set
        from sklearn.linear_model import LinearRegression
        reg = LinearRegression()
        reg.fit(X_train, y_train)
        
        #predicting the Test set result
        y_pred = reg.predict(X_test)
        o = df['open'].values
        h = df['high'].values
        l = df['low'].values

        n = len(df)
        
        pred = []
        for i in range(0,n):
            open = o[i]
            high = h[i]
            low = l[i]
            output = reg.predict([[open,high,low]])
            pred.append(output)

        pred1 = np.concatenate(pred)
        predicted = pred1.flatten().tolist()

        st.write("  ")
        st.write("  ")
        st.write("  ")
        t = predicted[-1]
        st.subheader("Your latest predicted closing price is: ")
        st.title(t)

    
    
    
    
        r2 = metrics.r2_score(y_test, y_pred)
        mae = metrics.mean_absolute_error(y_test, y_pred)
        mse = metrics.mean_squared_error(y_test, y_pred)
        rmse = mse**0.5
    
        col1, col2 = st.columns(2)
    
        col1.metric("R2 Score", r2, "± 5%")
        col2.metric("Mean Absolute Error ", mae, "± 5%")
        col1.metric("Mean Squared Error", mse, "± 5%")
        col2.metric("Root Mean Squared Error", rmse, "± 5%")

if __name__ == '__main__':
    main()
