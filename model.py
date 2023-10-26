import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.layers import LSTM, Dense
from sklearn.model_selection import TimeSeriesSplit
from keras.models import Sequential
import yfinance as yf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

# Ask the user to enter the stock code
stock_code = input("Enter the stock code (e.g., MSFT for Microsoft): ")

# Fetch stock data
stock = yf.Ticker(stock_code)
data = stock.history(period="10y", auto_adjust=False)

# Save data to a CSV file
data.to_csv(f"{stock_code}StockData.csv")

# Load the fetched dataset
try:
    df = pd.read_csv(f"{stock_code}StockData.csv", index_col='Date', parse_dates=True)
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("File not found or invalid format. Please make sure the file exists and is in CSV format.")
    exit(1)

# Print the shape of Dataframe and Check for Null Values
print("Dataframe Shape: ", df.shape)
print("Null Value Present: ", df.isnull().values.any())
print(df.columns)

# Set Target Variable
output_var = pd.DataFrame(df['Close'])
# Selecting the Features
features = ['Open', 'High', 'Low', 'Volume']

# Scaling
scaler = MinMaxScaler()
feature_transform = scaler.fit_transform(df[features])
feature_transform = pd.DataFrame(columns=features, data=feature_transform, index=df.index)
print(feature_transform.head())

# Splitting to Training set and Test set
timesplit = TimeSeriesSplit(n_splits=5)

# Initialize lists to store true and predicted values for each fold
true_values = []
predicted_values = []

for train_index, test_index in timesplit.split(feature_transform):
    X_train, X_test = feature_transform[:len(train_index)], feature_transform[len(train_index): (len(train_index)+len(test_index))]
    y_train, y_test = output_var[:len(train_index)].values.ravel(), output_var[len(train_index): (len(train_index)+len(test_index))].values.ravel()

    # Process the data for LSTM
    trainX = np.array(X_train)
    testX = np.array(X_test)
    X_train = trainX.reshape(X_train.shape[0], 1, X_train.shape[1])
    X_test = testX.reshape(X_test.shape[0], 1, X_test.shape[1])

    # Building the LSTM Model
    lstm = Sequential()
    lstm.add(LSTM(32, input_shape=(1, trainX.shape[1]), activation='relu', return_sequences=False))
    lstm.add(Dense(1))
    lstm.compile(loss='mean_squared_error', optimizer='adam')

    history = lstm.fit(X_train, y_train, epochs=50, batch_size=16, verbose=0, shuffle=False)

    y_pred = lstm.predict(X_test)

    # Store the true and predicted values for each fold
    true_values.append(y_test)
    predicted_values.append(y_pred)

# Display all the plots at once
plt.figure(figsize=(12, 6))  # Adjust the figure size as needed
for i in range(len(true_values)):
    plt.subplot(2, 3, i + 1)  # Create subplots for each fold
    plt.plot(true_values[i], label='True Value')
    plt.plot(predicted_values[i], label='LSTM Value')
    plt.title(f'Fold {i + 1}')
    plt.xlabel('Time Scale')
    plt.ylabel('Scaled USD')
    plt.legend()

plt.tight_layout()
plt.show()