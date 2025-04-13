
from datetime import datetime
from backend.extension import dbs as db

class StockHistory(db.Model):
    __tablename__ = 'stock_history'
    
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    average_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    stock = db.relationship('Stock', backref='history', lazy= True)
    
    def __repr__(self):
        return f"<StockHistory {self.id}, {self.stock_id}, {self.date}, {self.average_price}>"