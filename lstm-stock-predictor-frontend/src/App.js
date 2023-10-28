import React, { useState } from 'react';
import './App.css';

function App() {
  const [stockCode, setStockCode] = useState('');
  const [predictedValues, setPredictedValues] = useState([]);
  const [loading, setLoading] = useState(false);
  const [plotData, setPlotData] = useState(''); // State to hold the plot data


  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); // Set loading to true when the request is initiated.

    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ stock_code: stockCode }),
    });

    if (response.ok) {
      const data = await response.json();
      setPredictedValues(data.predicted_values);
      setPlotData(data.plot_data); // Set the plot data received from the server

    }

    setLoading(false); // Set loading to false when the response is received.
  };

  return (
    <div className="App">
      <h1>LSTM Stock Price Predictor</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="stockCode">Enter the stock code (e.g., MSFT for Microsoft):</label>
        <input
          type="text"
          id="stockCode"
          value={stockCode}
          onChange={(e) => setStockCode(e.target.value)}
          required
        />
        <button type="submit">Predict</button>
      </form>
      {loading && <p>Loading...</p>} {/* Display loading indicator when loading is true */}
      {!loading && predictedValues.length > 0 && (
        <div className="prediction-results">
          {plotData && <img src={`data:image/png;base64,${plotData}`} alt="Plot" />} {/* Display the plot */}
          <h2>Predicted Stock Prices:</h2>
          <ul>
            {predictedValues.map((value, index) => (
              <li key={index}>{value}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
