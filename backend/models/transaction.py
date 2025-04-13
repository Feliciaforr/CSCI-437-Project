from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from backend.extension import dbs as db

class Transaction(db.Model):
    """Transaction model for recording stock transactions.

    Tracks buy and sell transactions for users, including stock details, quantity, price, and timestamps.
    Establishes relationships with the Stock and User models.

    Fields:
    - `id`: unique identifier for the transaction.
    - `stock_id`: foreign key referencing the Stock model.
    - `user_id`: foreign key referencing the User model.
    - `transaction_type`: type of transaction ('buy' or 'sell').
    - `quantity`: number of stocks involved in the transaction.
    - `price`: price of the stock during the transaction.
    - `timestamp`: timestamp for when the transaction occurred.
    """
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)  # 'buy' or 'sell'
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False)
    stock = db.relationship('Stock', backref='transactions')
    user = db.relationship('User', backref='transactions')
    
    
    def __repr__(self):
        return f"<Transaction {self.id}, {self.stock_id}, {self.user_id}, {self.transaction_type}, {self.quantity}, {self.price}, {self.timestamp}>"