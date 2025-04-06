from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from extensiton import dbs as db

class Stock(db.Model):
    """Stock model for managing stock information.

    Stores details about stocks, including name, symbol, current price, and last updated timestamp.

    Fields:
    - `id`: unique identifier for the stock.
    - `name`: name of the stock, must be unique.
    - `symbol`: stock ticker symbol, must be unique.
    - `current_price`: current price of the stock.
    - `last_updated`: timestamp for the last update, auto-updated on modification.
    """
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
