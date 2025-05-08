import unittest
from datetime import datetime
from flask import Flask
from backend.extension import dbs as db
from backend.models.alerts import Alert
from backend.models.user import User  # Assuming the User model exists
from backend.models.stock import Stock  # Assuming the Stock model exists

class TestAlertModel(unittest.TestCase):
    def setUp(self):
        # Create a minimal Flask app for SQLAlchemy context
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(self.app)
        self.app_context = self.app.app_context()  # Save the app context
        self.app_context.push()  # Push the app context to make it active
        db.create_all()  # Create tables

    def tearDown(self):
        # Clean up the database and pop the app context
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_alert(self):
        # Create mock User and Stock entries
        user = User(id=1, name="Test User")  # Assuming User has 'id' and 'name' fields
        stock = Stock(id=1, name="Test Stock")  # Assuming Stock has 'id' and 'name' fields
        db.session.add(user)
        db.session.add(stock)
        db.session.commit()

        # Create an Alert entry
        alert = Alert(
            user_id=1,
            stock_id=1,
            change_percentage=5.0,
            direction='up',
            triggered_at=datetime(2025, 5, 5, 12, 0, 0)
        )
        db.session.add(alert)
        db.session.commit()

        # Query the Alert entry
        saved_alert = Alert.query.first()

        # Assertions
        self.assertIsNotNone(saved_alert)
        self.assertEqual(saved_alert.user_id, 1)
        self.assertEqual(saved_alert.stock_id, 1)
        self.assertEqual(saved_alert.change_percentage, 5.0)
        self.assertEqual(saved_alert.direction, 'up')
        self.assertEqual(saved_alert.triggered_at, datetime(2025, 5, 5, 12, 0, 0))
        self.assertEqual(saved_alert.user.name, "Test User")  # Verifies the relationship with User
        self.assertEqual(saved_alert.stock.name, "Test Stock")  # Verifies the relationship with Stock

if __name__ == '__main__':
    unittest.main()
