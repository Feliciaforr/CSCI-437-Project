import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.models.stock import Stock, initial_stocks
from backend.models.stock_history import StockHistory
from backend.extension import dbs as db
from flask_sqlalchemy import SQLAlchemy
import yfinance as yf
from datetime import datetime
from flask import Flask
from dotenv import load_dotenv


# Initialize Flask app and database
app = Flask(__name__)
load_dotenv()

# Configure database connection
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
# Configure database URI
db_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db.init_app(app)




# Seed the database with default stocks if it's empty
def seed_database_if_empty():
    if Stock.query.count() == 0:
        for item in initial_stocks:
            s = Stock(
                symbol=item["symbol"],
                name=item["name"]
            )
            db.session.add(s)
        db.session.commit()
        print("Database seeded with default stocks.")

# Fetch historical stock data and store it in the database
def fetch_and_store_yahoo_history():
    with app.app_context():
        seed_database_if_empty()  # Ensure the database is seeded
        stocks = Stock.query.all()  # Get all stocks from the database
        
        for stock in stocks:
            try:
                # Fetch 5 years of daily historical data
                ticker = yf.Ticker(stock.symbol)
                data = ticker.history(period="5y", interval='1d')
                
                if data.empty:
                    print(f"No data found for {stock.symbol}")
                    continue
                
                for date_index, row in data.iterrows():
                    avg_price = (row['Open'] + row['Close']) / 2
                    
                    # Check if the record already exists
                    existing = StockHistory.query.filter_by(
                        stock_id = stock.id,
                        date=date_index.date()
                    ).first()

                    if not existing:
                        # Add new record if it doesn't exist
                        history = StockHistory(
                            stock_id=stock.id,
                            average_price=avg_price,
                            date=date_index.date(),
                            # last_updated=datetime.now()
                        )
                        db.session.add(history)
                        print("New added")
                
                print(f"Data for {stock.symbol} stored successfully.")
                
            except Exception as e:
                print(f"Error fetching data for {stock.symbol}: {e}")
        
        db.session.commit()
        print("All data fetched and stored successfully.")

# Main entry point
if __name__ == "__main__":
    with app.app_context():
        fetch_and_store_yahoo_history()
        
        
# This script initializes a Flask app, seeds the database with default stocks if empty, 
# and fetches 5 years of historical stock data using the Yahoo Finance API. 
# It ensures no duplicate records are added by checking for existing entries before inserting new ones. 
# The script is designed to maintain an up-to-date database for stock analysis and visualization.
