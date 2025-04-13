from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from backend.extension import dbs as db

class StockPriceToday(db.Model):
    """StockPriceToday model for tracking today's stock prices.

    Stores stock price details for today, including the stock symbol, price, and timestamps. 
    Tracks relationships with the Stock model.

    Fields:
    - `id`: unique identifier for the stock price entry.
    - `stock_id`: foreign key referencing the Stock model.
    - `symbol`: stock ticker symbol.
    - `time_stamp`: timestamp for the price entry.
    - `price`: current price of the stock.
    - `created_at`: timestamp for record creation or modification.
    """
    __tablename__ = 'stock_price_today'
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    time_stamp = db.Column(db.DateTime, nullable=False, default=datetime.now)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    date = db.Column(db.Date, nullable=False)
    
    stock = db.relationship('Stock', backref='stock_price_today', lazy=True)
    
    def __repr__(self):
        return f"<StockPriceToday {self.symbol} - {self.price}>"