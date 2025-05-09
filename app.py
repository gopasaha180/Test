import streamlit as st
import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the trained model (replace 'model02.pkl' with your actual model filename)
model02 = joblib.load('model02.pkl')

# Fetch S&P 500 data from Yahoo Finance
sp500 = yf.Ticker("^GSPC")
sp500 = sp500.history(period="max")
sp500.index = pd.to_datetime(sp500.index)
sp500.index = sp500.index.tz_localize(None)  # Remove timezone info
sp500.index = sp500.index.normalize()  # Normalize to midnight

# Add target column
sp500["Tomorrow"] = sp500["Close"].shift(-1)
sp500["Target"] = (sp500["Tomorrow"] > sp500["Close"]).astype(int)
sp500 = sp500.dropna()  # Remove NaN values

# Streamlit UI
st.title("S&P 500 Market Prediction App")

# Example of taking user input (simplified version, can add more features as needed)
st.write("Enter market data for prediction:")
user_input = st.text_input("Enter Close price (last known market value)")

if st.button("Predict"):
    if user_input:
        # Convert user input to the appropriate format
        input_data = pd.DataFrame([[float(user_input), 1000000, 4000, 4100, 3900]],
                                  columns=["Close", "Volume", "Open", "High", "Low"])
        prediction = model02.predict(input_data)
        st.write(f"Prediction: {'Up' if prediction[0] == 1 else 'Down'}")
    else:
        st.write("Please enter a value to predict.")
