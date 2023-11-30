# lstm_stock_predictor.py

import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from sklearn.preprocessing import MinMaxScaler
from keras.layers import LSTM, Dense
from keras.models import Sequential
from sklearn.model_selection import TimeSeriesSplit
import yfinance as yf
import os
import tensorflow as tf
from io import BytesIO
# from tensorflow.keras.models import load_model
# import matplotlib.pyplot as plt
from flask_cors import CORS  # Import the 'CORS' extension
import base64
# to hide warning messages
import warnings

import pandas as pd
import threading  # Import the 'threading' module
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt


df = pd.read_csv('./tickers.csv')
list_of_tickers = df['DDD'].tolist()

warnings.filterwarnings('ignore')




app = Flask(__name__)
CORS(app)  # Enable CORS for your Flask app

# app = Flask(__name__)
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

def get_shape(my_list):
    if isinstance(my_list, list):
        if all(isinstance(sublist, list) for sublist in my_list):
            # It's a 2D list
            num_rows = len(my_list)
            num_cols = len(my_list[0]) if num_rows > 0 else 0
            return (num_rows, num_cols)
        else:
            # It's a 1D list
            num_rows = len(my_list)
            return (num_rows, 1)
    else:
        # It's not a list
        return None

def convert_to_json_serializable(data):
    if isinstance(data, list):
        # If it's a list, convert all its elements
        return [convert_to_json_serializable(item) for item in data]
    elif isinstance(data, np.ndarray):
        # If it's a NumPy array, convert it to a list
        return data.tolist()
    else:
        return data

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # return jsonify({'predicted_values': data['stock_code']})
    stock_code = data['stock_code']

    # Fetch stock data
    stock = yf.Ticker(stock_code)
    df = stock.history(period="10y", auto_adjust=False)

    # Data preprocessing
    output_var = pd.DataFrame(df['Close'])
    features = ['Open', 'High', 'Low', 'Volume']
    scaler = MinMaxScaler()
    feature_transform = scaler.fit_transform(df[features])
    feature_transform = pd.DataFrame(columns=features, data=feature_transform, index=df.index)

    # Splitting into Training set and Test set
    timesplit = TimeSeriesSplit(n_splits=10)

    true_values = []
    predicted_values = []

    for train_index, test_index in timesplit.split(feature_transform):
        X_train, X_test = feature_transform[:len(train_index)], feature_transform[len(train_index): (len(train_index) + len(test_index))]
        y_train, y_test = output_var[:len(train_index)].values.ravel(), output_var[len(train_index): (len(train_index) + len(test_index))].values.ravel()

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

        # Training the LSTM model
        history = lstm.fit(X_train, y_train, epochs=100, batch_size=16, verbose=1, shuffle=False)

        # Predicting stock prices
        y_pred = lstm.predict(X_test)

        # Store the true and predicted values for each fold
        true_values.append(y_test)
        predicted_values.append(y_pred)

    # Calculate the number of subplots dynamically based on the number of folds
    num_folds = len(true_values)
    num_rows = (num_folds // 3) + (1 if num_folds % 3 != 0 else 0)
    num_cols = min(num_folds, 3)

    # Create subplots dynamically
    plt.figure(figsize=(12, 6))  # Adjust the figure size as needed
    for i in range(num_folds):
        plt.subplot(num_rows, num_cols, i + 1)  # Create subplots for each fold
        plt.plot(true_values[i], label='True Value')
        plt.plot(predicted_values[i], label='LSTM Value')
        plt.title(f'Fold {i + 1}')
        plt.xlabel('Time Scale')
        plt.ylabel('Scaled USD')
        plt.legend()

    
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')


    shape_1d = get_shape(predicted_values)
    print(f"Shape of our list: {shape_1d}")
    # print(predicted_values.sha)
    # return jsonify({'predicted_values': "success"})
    # return jsonify(predicted_values)
    # return jsonify({'predicted_values': predicted_values})
    # Convert predicted_values to JSON serializable format
    serializable_values = convert_to_json_serializable(predicted_values)

    # Return the predicted values as JSON
    return jsonify({'predicted_values': serializable_values, 'plot_data': plot_data, 'list_of_tickers': list_of_tickers})



# if __name__ == '__main':
#     app.run(debug=True)

def run_flask_server():
    app.run(debug=True)

if __name__ == '__main__':
    # Suppress warnings related to TensorFlow (optional)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

    # Start the Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask_server)
    flask_thread.daemon = True  # Make the thread a daemon to stop it when the main program exits
    flask_thread.start()

    # Your non-GUI code can go here
    # Continue with other code

    # You can wait for the Flask thread to finish (optional)
    flask_thread.join()


# from flask import Flask, request, jsonify
# from tensorflow.python.keras.models import Sequential
# # from tensorflow.keras.layers import LSTM, Dense
# from tensorflow.python.keras.layers import LSTM, Dense
# import numpy as np
# import pandas as pd

# app = Flask(__name__)

# # Dictionary to store models
# model_dict = {}

# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.get_json()
#     stock_code = data['stock_code']
#     date_interval = data['date_interval']
#     input_data = np.array(data['input_data'])

#     if (stock_code, date_interval) not in model_dict:
#         # Model for this combination doesn't exist, create and train it
#         model = build_and_train_model(stock_code, date_interval)
#         model_dict[(stock_code, date_interval)] = model

#     # Retrieve the model for prediction
#     lstm_model = model_dict[(stock_code, date_interval)]

#     # Make predictions with the model
#     predicted_values = lstm_model.predict(input_data)

#     # Return the predicted values
#     return jsonify({'predicted_values': predicted_values.tolist()})

# def build_and_train_model(stock_code, date_interval):
#     # Fetch historical data for the specified stock code and date interval
#     # historical_data = fetch_historical_data(stock_code, date_interval)
#     historical_data = yf.Ticker(stock_code)
#     # stock = yf.Ticker(stock_code)
# #     df = stock.history(period="10y", auto_adjust=False)

#     # Create and train the LSTM model using the historical data
#     model = Sequential()
#     model.add(LSTM(32, input_shape=(1, historical_data.shape[1]), activation='relu', return_sequences=False))
#     model.add(Dense(1))
#     model.compile(loss='mean_squared_error', optimizer='adam')

#     # Train the model (replace this with your actual training process)
#     model.fit(historical_data, y_train, epochs=50, batch_size=16, verbose=0, shuffle=False)

#     return model
# def fetch_historical_data(stock_code, date_interval):
#     try:
#         # Load historical stock data from the CSV file
#         df = pd.read_csv(data_file_path)
        
#         # Filter data based on stock code and date interval
#         filtered_data = df[(df['stock_code'] == stock_code) & (df['date_interval'] == date_interval)]
        
#         # Extract relevant features and convert to a numpy array
#         features = ['Open', 'High', 'Low', 'Volume']
#         historical_data = filtered_data[features].values
        
#         return historical_data
#     except FileNotFoundError:
#         # Handle file not found error
#         return None

# if __name__ == '__main__':
#     app.run(debug=True)

