from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from backend.extension import dbs as db

"""Portfolio model for tracking user stock holdings.

Represents the stocks held by a user, including the quantity and average purchase price.
Establishes relationships with the User and Stock models.

Fields:
- `id`: unique identifier for the portfolio entry.
- `user_id`: foreign key referencing the User model.
- `stock_id`: foreign key referencing the Stock model.
- `quantity`: number of stocks held by the user.
- `average_price`: average purchase price of the stocks.
"""

class Portfolio(db.Model):
    __tablename__ = 'portfolios'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    average_price = db.Column(db.Float, nullable=False)
    
    
    
    def __repr__(self):
        return f"<Portfolio {self.id}, {self.user_id}, {self.stock_id}, {self.quantity}, {self.average_price}>"