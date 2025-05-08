import unittest
from datetime import date, datetime
from backend.models.stock_history import StockHistory
from backend.extension import dbs as db
from backend.models.stock import Stock  # Assuming the Stock model exists
from flask import Flask

class TestStockHistoryModel(unittest.TestCase):
    def setUp(self):
        # Set up a Flask app and an in-memory SQLite database
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(self.app)

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up the database
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_stock_history_creation(self):
        with self.app.app_context():
            # Create a mock Stock entry
            stock = Stock(id=1, name="Test Stock")  # Assuming Stock has 'id' and 'name' fields
            db.session.add(stock)
            db.session.commit()

            # Create a StockHistory entry
            stock_history = StockHistory(
                stock_id=1,
                date=date(2025, 5, 5),
                average_price=150.75,
                created_at=datetime(2025, 5, 5, 12, 0, 0)
            )
            db.session.add(stock_history)
            db.session.commit()

            # Query the StockHistory entry
            result = StockHistory.query.first()

            # Assertions
            self.assertIsNotNone(result)
            self.assertEqual(result.stock_id, 1)
            self.assertEqual(result.date, date(2025, 5, 5))
            self.assertEqual(result.average_price, 150.75)
            self.assertEqual(result.created_at, datetime(2025, 5, 5, 12, 0, 0))
            self.assertEqual(result.stock.name, "Test Stock")  # Verifies the relationship

if __name__ == '__main__':
    unittest.main()