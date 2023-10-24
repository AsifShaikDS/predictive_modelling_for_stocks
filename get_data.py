import yfinance as yf

# Fetch Microsoft stock data
msft = yf.Ticker("MSFT")

# Get historical data
data = msft.history(period="23y")  # Replace "5d" with your desired time period

# Save data to a CSV file
data.to_csv("MicrosoftStockData.csv")
