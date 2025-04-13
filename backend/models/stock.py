from flask_sqlalchemy import SQLAlchemy
from backend.extension import dbs as db

class Stock(db.Model):
    """Stock model for managing static stock metadata.

    Stores reference data for each stock.

    Fields:
    - `id`: unique identifier for the stock.
    - `name`: full name of the company (unique).
    - `symbol`: stock ticker symbol (unique).
    """
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    symbol = db.Column(db.String(10), nullable=False, unique=True)

# List of predefined stocks for initial seeding
initial_stocks = [
    {"name": "Apple Inc.", "symbol": "AAPL"},
    {"name": "Microsoft Corporation", "symbol": "MSFT"},
    {"name": "Amazon.com, Inc.", "symbol": "AMZN"},
    {"name": "Alphabet Inc. (Class A)", "symbol": "GOOGL"},
    {"name": "Meta Platforms, Inc.", "symbol": "META"},
    {"name": "Tesla, Inc.", "symbol": "TSLA"},
    {"name": "NVIDIA Corporation", "symbol": "NVDA"},
    {"name": "JPMorgan Chase & Co.", "symbol": "JPM"},
    {"name": "Johnson & Johnson", "symbol": "JNJ"},
    {"name": "Visa Inc.", "symbol": "V"},
    {"name": "Procter & Gamble Co.", "symbol": "PG"},
    {"name": "Walmart Inc.", "symbol": "WMT"},
    {"name": "Mastercard Incorporated", "symbol": "MA"},
    {"name": "UnitedHealth Group", "symbol": "UNH"},
    {"name": "Bank of America Corporation", "symbol": "BAC"},
    {"name": "Home Depot, Inc.", "symbol": "HD"},
    {"name": "Pfizer Inc.", "symbol": "PFE"},
    {"name": "Coca-Cola Company", "symbol": "KO"},
    {"name": "Netflix, Inc.", "symbol": "NFLX"},
    {"name": "Intel Corporation", "symbol": "INTC"},
]