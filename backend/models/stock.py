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
    {"name": "Alphabet Inc.", "symbol": "GOOGL"},
    {"name": "Amazon.com Inc.", "symbol": "AMZN"},
    {"name": "Tesla Inc.", "symbol": "TSLA"},
    {"name": "NVIDIA Corporation", "symbol": "NVDA"},
    {"name": "Meta Platforms Inc.", "symbol": "META"},
    {"name": "Netflix Inc.", "symbol": "NFLX"},
    {"name": "Advanced Micro Devices Inc.", "symbol": "AMD"},
    {"name": "Intel Corporation", "symbol": "INTC"},
    {"name": "Alibaba Group Holding Ltd.", "symbol": "BABA"},
    {"name": "PayPal Holdings Inc.", "symbol": "PYPL"},
    {"name": "Uber Technologies Inc.", "symbol": "UBER"},
    {"name": "The Walt Disney Company", "symbol": "DIS"},
    {"name": "PepsiCo Inc.", "symbol": "PEP"},
    {"name": "The Coca-Cola Company", "symbol": "KO"},
    {"name": "JPMorgan Chase & Co.", "symbol": "JPM"},
    {"name": "Walmart Inc.", "symbol": "WMT"},
    {"name": "Chevron Corporation", "symbol": "CVX"},
    {"name": "Palantir Technologies Inc.", "symbol": "PLTR"},
]