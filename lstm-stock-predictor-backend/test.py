from flask import Flask, request, jsonify
import requests

client_app = Flask(__name__)

@client_app.route('/send_data', methods=['POST'])
def send_data():
    # Define your 2D list
    data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    return jsonify(data)

    # Define the server-side Flask API endpoint
    # server_url = 'http://localhost:5000/process_data'  # Replace with your server's URL

    # # Send the data as JSON in a POST request to the server
    # response = requests.post(server_url, json=data)

    # if response.status_code == 200:
    #     result = response.json()
        # return jsonify(result)
    # else:
    #     return jsonify({'error': 'Failed to send data'})

if __name__ == '__main__':
    client_app.run()  # Run on a different port
