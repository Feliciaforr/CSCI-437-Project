import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import requests
from datetime import datetime, timedelta, timezone
from backend.extension import dbs as db
from dotenv import load_dotenv
from backend.models import Stock, StockPriceToday, StockCurrentprice
from flask import Flask
import yfinance as yf

# Initialize Flask app and database
app = Flask(__name__)
load_dotenv()

# Configure database connection
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db.init_app(app)

# Finnhub API configuration
FINHUB_API_KEY = os.getenv('FINHUB_API_KEY')
FINNHUB_URL = "https://finnhub.io/api/v1/stock/candle"

# Test connection with a specific time range
est_offset = timedelta(hours=-4)
from_dt = datetime(2025, 4, 11, 9, 30, tzinfo=timezone(est_offset))  # Start of trading day
to_dt = datetime(2025, 4, 11, 14, 0, tzinfo=timezone(est_offset))  # Midday
FROM_UNIX = int(from_dt.timestamp())
TO_UNIX = int(to_dt.timestamp())

# Function to fetch and store intraday data (runs once at the start of the day)
def fetch_and_store_intraday_data():
    with app.app_context():
        # Clear existing intraday data to avoid duplicates
        db.session.query(StockPriceToday).delete()
        db.session.query(StockCurrentprice).delete()
        db.session.commit()

        stocks = Stock.query.all()  # Fetch all stocks from the database

        for stock in stocks:
            try:
                # Fetch intraday data (5-minute intervals) for the current day
                ticker = yf.Ticker(stock.symbol)
                data = ticker.history(period='1d', interval='5m')

                if data.empty:  # Skip if no data is available
                    print(f"No intraday data found for {stock.symbol}")
                    continue

                # Store intraday data in StockPriceToday
                for index, row in data.iterrows():
                    avg_price = (row['High'] + row['Low']) / 2  # Calculate average price
                    new_record = StockPriceToday(
                        stock_id=stock.id,
                        symbol=stock.symbol,
                        time_stamp=index.to_pydatetime(),
                        price=avg_price,
                        date=index.date()
                    )
                    db.session.add(new_record)

                # Store the latest price in StockCurrentprice
                last_row = data.iloc[-1]
                avg_price = (last_row['High'] + last_row['Low']) / 2
                db.session.add(StockCurrentprice(
                    stock_id=stock.id,
                    price=avg_price,
                    timestamp=datetime.now()
                ))

                db.session.commit()  # Commit changes for the current stock
                print(f"Intraday data for {stock.symbol} saved successfully.")

            except Exception as e:  # Handle errors during data fetching
                print(f"Error fetching data for {stock.symbol}: {e}")

        print("All intraday data saved successfully using Yahoo Finance.")

# Function to update current prices (runs every 20 seconds)
def update_current_prices_only():
    with app.app_context():
        stocks = Stock.query.all()  # Fetch all stocks from the database

        for stock in stocks:
            params = {
                "symbol": stock.symbol,
                "token": FINHUB_API_KEY
            }

            # Fetch the current price from Finnhub API
            response = requests.get("https://finnhub.io/api/v1/quote", params=params)
            data = response.json()

            if not data.get("c"):  # Skip if no current price is available
                print(f"Failed to fetch current price for {stock.symbol}")
                continue

            current_price = data["c"]  # Current price
            now = datetime.now()  # Current timestamp

            # Update or insert into StockCurrentprice
            # existing = StockCurrentprice.query.filter_by(stock_id=stock.id).first()
            # if existing:
            #     existing.price = current_price
            #     existing.timestamp = now
            # else:
            db.session.add(StockCurrentprice(
                    stock_id=stock.id,
                    price=current_price,
                    timestamp=now
                ))

            # Append the current price to StockPriceToday
            db.session.add(StockPriceToday(
                stock_id=stock.id,
                symbol=stock.symbol,
                time_stamp=now,
                price=current_price,
                date=now.date()
            ))

        db.session.commit() 
        # Commit all changes
        after = db.session.query(StockPriceToday).count()
        print(after)
        print("Live prices are being updated every 20 seconds.")

"""
This script integrates with Yahoo Finance and Finnhub APIs to manage stock price data.

1. `fetch_and_store_intraday_data`:
   Runs once at the start of the trading day.
   Fetches intraday stock prices (5-minute intervals) for all stocks.
   Stores the data in `StockPriceToday` and the latest price in `StockCurrentprice`.

2. `update_current_prices_only`:
   Runs every 20 seconds during the trading day.
   Fetches the current stock price for all stocks from the Finnhub API.
   Updates `StockCurrentprice` with the latest price.
   Appends the current price to `StockPriceToday`.

The script ensures the database is always up-to-date with intraday and live stock prices for analysis and visualization.
"""
