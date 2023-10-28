// import React, { useState } from 'react';
// import './App.css';

// function App() {
//   const [stockCode, setStockCode] = useState('');
//   const [predictedValues, setPredictedValues] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [plotData, setPlotData] = useState(''); // State to hold the plot data

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setLoading(true); // Set loading to true when the request is initiated.

//     const response = await fetch('http://localhost:5000/predict', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ stock_code: stockCode }),
//     });

//     if (response.ok) {
//       const data = await response.json();
//       setPredictedValues(data.predicted_values);
//       setPlotData(data.plot_data); // Set the plot data received from the server

//     }

//     setLoading(false); // Set loading to false when the response is received.
//   };

//   return (
//     <div className="App">
//       <h1>LSTM Stock Price Predictor</h1>
//       <form onSubmit={handleSubmit}>
//         <label htmlFor="stockCode">Enter the stock code (e.g., MSFT for Microsoft):</label>
//         <input
//           type="text"
//           id="stockCode"
//           value={stockCode}
//           onChange={(e) => setStockCode(e.target.value)}
//           required
//         />
//         <button type="submit">Predict</button>
//       </form>
//       {loading && <p>Loading...</p>} {/* Display loading indicator when loading is true */}
//       {!loading && predictedValues.length > 0 && (
//         <div className="prediction-results">
//           {plotData && <img src={`data:image/png;base64,${plotData}`} alt="Plot" />} {/* Display the plot */}
//           <h2>Predicted Stock Prices:</h2>
//           <ul>
//             {predictedValues.map((value, index) => (
//               <li key={index}>{value}</li>
//             ))}
//           </ul>
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;

import React, { useState } from "react";
import "./App.css";
import { Form, Input, Button, Spin, List, Typography, Card } from "antd";

function App() {
  const [stockCode, setStockCode] = useState("");
  const [predictedValues, setPredictedValues] = useState([]);
  const [loading, setLoading] = useState(false);
  const [plotData, setPlotData] = useState(""); // State to hold the plot data

  const onFinish = async () => {
    setLoading(true);

    const response = await fetch("http://localhost:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ stock_code: stockCode }),
    });

    if (response.ok) {
      const data = await response.json();
      setPredictedValues(data.predicted_values);
      setPlotData(data.plot_data);
    }

    setLoading(false);
  };

  return (
    <div className="App">
      <h1
        style={{
          textAlign: "center",
          margin: "20px 0",
          fontSize: "33px",
          color: "#ff8718", // You can choose your desired text color
          textTransform: "uppercase", // Uppercase text
        }}
      >
        LSTM Stock Price Predictor
      </h1>
      <div style={{ display: "flex", justifyContent: "center" }}>
        <Card
          title="Stock Price Prediction"
          style={{
            width: "400px",
            border: "2px solid #1890ff",
            borderRadius: "10px",
          }}
        >
          <Form name="stockCodeForm" onFinish={onFinish} layout="vertical">
            <Form.Item
              label="Enter the stock code (e.g., MSFT for Microsoft):"
              name="stockCode"
              rules={[{ required: true, message: "Please enter a stock code" }]}
            >
              <Input
                value={stockCode}
                onChange={(e) => setStockCode(e.target.value)}
              />
            </Form.Item>
            <Form.Item>
              <Button type="primary" htmlType="submit" loading={loading}>
                Predict
              </Button>
            </Form.Item>
          </Form>
          {loading && <Spin size="large" />}
        </Card>
      </div>
      {plotData && <img src={`data:image/png;base64,${plotData}`} alt="Plot" />}
    </div>
  );
}

export default App;
