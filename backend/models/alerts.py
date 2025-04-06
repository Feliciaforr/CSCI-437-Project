from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from extensiton import dbs as db

"""Alert model for tracking stock alerts.

Represents alerts set by users for stock price changes, including the percentage change, direction, and trigger timestamp.
Establishes relationships with the User and Stock models.

Fields:
- `id`: unique identifier for the alert.
- `user_id`: foreign key referencing the User model
.
- `stock_id`: foreign key referencing the Stock model.
- `change_percentage`: percentage change in stock price to trigger the alert.
- `direction`: direction of the change ('up' or 'down').
- `triggered_at`: timestamp for when the alert was triggered.
"""

class Alert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'), nullable=False)
    change_percentage = db.Column(db.Float, nullable=False)
    direction = db.Column(db.String(10), nullable=False)  # 'up' or 'down'
    triggered_at = db.Column(db.DateTime,default = datetime.now, nullable=True)
    
    user = db.relationship('User', backref='alerts')
    stock = db.relationship('Stock', backref='alerts')
    
    def __repr__(self):
        return f"<Alert {self.id}, {self.user_id}, {self.stock_id}, {self.change_percentage}, {self.direction}, {self.triggered_at}>"