# from flask import Flask, request, jsonify
# import requests

# client_app = Flask(__name__)

# @client_app.route('/send_data', methods=['POST'])
# def send_data():
#     # Define your 2D list
#     data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
#     return jsonify(data)

#     # Define the server-side Flask API endpoint
#     # server_url = 'http://localhost:5000/process_data'  # Replace with your server's URL

#     # # Send the data as JSON in a POST request to the server
#     # response = requests.post(server_url, json=data)

#     # if response.status_code == 200:
#     #     result = response.json()
#         # return jsonify(result)
#     # else:
#     #     return jsonify({'error': 'Failed to send data'})

# if __name__ == '__main__':
#     client_app.run()  # Run on a different port

import numpy as np
import pandas as pd
import datetime
import pandas_datareader.data as web
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Define the stock and the date range for historical data
stock_symbol = 'AAPL'  # Change this to your desired stock symbol
start_date = '2010-01-01'
end_date = '2020-12-31'

# Fetch historical stock data using pandas_datareader
stock_data = web.DataReader(stock_symbol, data_source='yahoo', start=start_date, end=end_date)

# Create a DataFrame with the 'Adj Close' prices
df = pd.DataFrame(data=stock_data['Adj Close'])

# Create a new column for the "Prediction" shifted 'n' units up
n = 30  # Number of days to shift for prediction
df['Prediction'] = df[['Adj Close']].shift(-n)

# Create the feature dataset (X) and the target dataset (y)
X = np.array(df.drop(['Prediction'], 1))
X = X[:-n]
y = np.array(df['Prediction'])
y = y[:-n]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Create and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Get the last 'n' rows of the feature dataset
x_forecast = X[-n:]

# Make predictions for the next 'n' days
y_pred = model.predict(x_forecast)

# Plot the predictions and the actual data
plt.figure(figsize=(12, 6))
plt.plot(df.index[-n:], y_pred, label="Predicted Prices")
plt.plot(df.index[-n:], df['Adj Close'][-n:], label="Actual Prices")
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.legend()
plt.show()

