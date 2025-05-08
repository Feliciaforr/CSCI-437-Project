import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask
from unittest.mock import patch, MagicMock
from datetime import datetime
from backend.alerts.alert_logic import start_alert_checks, create_alert
from backend.models import Stock, StockHistory, StockPriceToday, Alert
from backend.extension import dbs as db

class TestAlertLogic(unittest.TestCase):
    def setUp(self):
        # Mock the app context
        self.app_patcher = patch("backend.alerts.alert_logic.app.app_context")
        self.mock_app_context = self.app_patcher.start()
        self.mock_app_context.return_value.__enter__.return_value = None

        # Mock the database session
        self.db_session_patcher = patch("backend.alerts.alert_logic.db.session")
        self.mock_db_session = self.db_session_patcher.start()

    def tearDown(self):
        # Stop all patches
        self.app_patcher.stop()
        self.db_session_patcher.stop()

    @patch("backend.alerts.alert_logic.Stock.query")
    @patch("backend.alerts.alert_logic.StockHistory.query")
    @patch("backend.alerts.alert_logic.StockPriceToday.query")
    def test_start_alert_checks(self, mock_stock_price_query, mock_stock_history_query, mock_stock_query):
        # Mock Stock entries
        mock_stock = MagicMock(id=1, symbol="TEST")
        mock_stock_query.all.return_value = [mock_stock]

        # Mock StockHistory entries
        mock_stock_history = MagicMock(stock_id=1, average_price=100.0, date=datetime(2025, 5, 5))
        mock_stock_history_query.filter_by.return_value.order_by.return_value.first.return_value = mock_stock_history

        # Mock StockPriceToday entries
        mock_stock_price = MagicMock(stock_id=1, price=110.0, time_stamp=datetime(2025, 5, 5, 12, 0, 0))
        mock_stock_price_query.filter_by.return_value.order_by.return_value.first.return_value = mock_stock_price

        # Mock create_alert to avoid actual database interaction
        with patch("backend.alerts.alert_logic.create_alert") as mock_create_alert, \
             patch("time.sleep", return_value=None):  # Prevent infinite loop
            start_alert_checks(max_iterations=3)

            # Verify baseline price was set
            mock_stock_history_query.filter_by.assert_called_with(stock_id=1)
            self.assertEqual(mock_stock_history.average_price, 100.0)

            # Verify alert creation for upward movement
            mock_create_alert.assert_called_with(1, 10.0, 'up')

    @patch("backend.alerts.alert_logic.Stock.query")
    @patch("backend.alerts.alert_logic.StockHistory.query")
    @patch("time.sleep", return_value=None)  # Mock time.sleep to avoid delays
    def test_start_alert_checks_terminates(self, mock_sleep, mock_stock_history_query, mock_stock_query):
        # Mock Stock entries
        mock_stock = MagicMock(id=1, symbol="TEST")
        mock_stock_query.all.return_value = [mock_stock]

        # Mock StockHistory entries
        mock_stock_history = MagicMock(stock_id=1, average_price=100.0, date=datetime(2025, 5, 5))
        mock_stock_history_query.filter_by.return_value.order_by.return_value.first.return_value = mock_stock_history

        # Run the function with a termination condition
        start_alert_checks(max_iterations=3)

        # Verify that the loop ran the expected number of iterations
        self.assertEqual(mock_sleep.call_count, 3)  # time.sleep should be called 3 times

    @patch("backend.alerts.alert_logic.db.session")
    def test_create_alert(self, mock_db_session):
        # Call create_alert
        create_alert(stock_id=1, percent_change=5.0, direction="up")

        # Verify that an Alert object was added to the session
        mock_db_session.add.assert_called_once()
        added_alert = mock_db_session.add.call_args[0][0]
        self.assertIsInstance(added_alert, Alert)
        self.assertEqual(added_alert.stock_id, 1)
        self.assertEqual(added_alert.change_percentage, 5.0)
        self.assertEqual(added_alert.direction, "up")
        self.assertIsInstance(added_alert.triggered_at, datetime)

        # Verify that the session was committed
        mock_db_session.commit.assert_called_once()

if __name__ == '__main__':
    # Run the tests and print a custom message
    result = unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(TestAlertLogic))
    if result.wasSuccessful():
        print(f"\nRan {result.testsRun} test(s) successfully.")
        print("Test Passed")
    else:
        print("\nSome tests failed.")
