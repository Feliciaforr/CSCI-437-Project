import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from backend.routes.suggestions import get_suggestions
from backend.models import Stock, StockCurrentprice, StockHistory

class TestSuggestions(unittest.TestCase):
    def setUp(self):
        # Create a minimal Flask app for testing
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    @patch("backend.routes.suggestions.Stock.query")
    @patch("backend.routes.suggestions.StockHistory.query")
    @patch("backend.routes.suggestions.StockCurrentprice.query")
    @patch("flask_jwt_extended.view_decorators.verify_jwt_in_request")
    def test_get_suggestions(self, mock_verify_jwt, mock_currentprice_query, mock_history_query, mock_stock_query):
        # Mock Stock entries
        mock_stock = MagicMock(id=1, symbol="TEST", name="Test Stock")
        mock_stock_query.all.return_value = [mock_stock]

        # Mock StockHistory entries
        mock_history_entries = [
            MagicMock(average_price=100.0),
            MagicMock(average_price=102.0),
            MagicMock(average_price=98.0),
            MagicMock(average_price=101.0),
            MagicMock(average_price=99.0),
        ]
        mock_history_query.filter_by.return_value.order_by.return_value.limit.return_value.all.return_value = mock_history_entries

        # Mock StockCurrentprice entry
        mock_current_entry = MagicMock(price=95.0)
        mock_currentprice_query.filter_by.return_value.order_by.return_value.first.return_value = mock_current_entry

        # Call the function
        with self.app.test_request_context():
            response = get_suggestions()

        # Assertions
        self.assertEqual(response.status_code, 200)
        suggestions = response.json
        self.assertEqual(len(suggestions), 1)  # Only one stock was mocked
        self.assertEqual(suggestions[0]["symbol"], "TEST")
        self.assertEqual(suggestions[0]["name"], "Test Stock")
        self.assertEqual(suggestions[0]["current_price"], 95.0)
        self.assertEqual(suggestions[0]["moving_average"], 100.0)
        self.assertEqual(suggestions[0]["suggestion"], "BUY")

if __name__ == "__main__":
    unittest.main()
