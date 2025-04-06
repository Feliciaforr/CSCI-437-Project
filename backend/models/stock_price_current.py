from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from extensiton import dbs as db


class StockCurrentprice(db.Model):
    """StockCurrentprice model for tracking the current price of stocks.

    Stores the latest price of a stock along with a timestamp and links to the Stock model.

    Fields:
    - `id`: unique identifier for the price entry.
    - `stock_id`: foreign key referencing the Stock model.
    - `price`: current price of the stock.
    - `timestamp`: timestamp for when the price was recorded.
    """
    __tablename__ = 'stock_current_price'
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    stock = db.relationship('Stock', backref='current_prices')
    
    def __repr__(self):
        return f"<StockCurrentprice {self.stock_id}, {self.price}, {self.timestamp}>"