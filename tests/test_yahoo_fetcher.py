import unittest
from unittest.mock import patch, MagicMock
from backend.market.yahoo_fetcher import fetch_and_store_yahoo_history, seed_database_if_empty
from backend.models.stock import Stock
from backend.models.stock_history import StockHistory
from backend.extension import dbs as db

class TestYahooFetcher(unittest.TestCase):
    def setUp(self):
        # Mock the Flask app context
        self.app_patcher = patch("backend.market.yahoo_fetcher.app.app_context")
        self.mock_app_context = self.app_patcher.start()
        self.mock_app_context.return_value.__enter__.return_value = None

        # Mock the database session
        self.db_session_patcher = patch("backend.market.yahoo_fetcher.db.session")
        self.mock_db_session = self.db_session_patcher.start()

    def tearDown(self):
        # Stop all patches
        self.app_patcher.stop()
        self.db_session_patcher.stop()

    @patch("backend.market.yahoo_fetcher.Stock.query")
    @patch("backend.market.yahoo_fetcher.yf.Ticker")
    def test_fetch_and_store_yahoo_history(self, mock_ticker, mock_stock_query):
        # Mock Stock entries
        mock_stock = MagicMock(id=1, symbol="AAPL", name="Apple Inc.")
        mock_stock_query.all.return_value = [mock_stock]

        # Mock Yahoo Finance API response
        mock_ticker_instance = MagicMock()
        mock_ticker.return_value = mock_ticker_instance
        mock_ticker_instance.history.return_value = MagicMock(
            iterrows=lambda: iter([
                (datetime(2025, 5, 5), {"Open": 150.0, "Close": 155.0}),
                (datetime(2025, 5, 6), {"Open": 152.0, "Close": 158.0}),
            ])
        )

        # Mock StockHistory query to simulate no existing records
        mock_stock_history_query = patch("backend.market.yahoo_fetcher.StockHistory.query").start()
        mock_stock_history_query.filter_by.return_value.first.return_value = None

        # Call the function
        fetch_and_store_yahoo_history()

        # Verify that the database was seeded
        self.assertTrue(mock_stock_query.all.called)

        # Verify that the Yahoo Finance API was called
        mock_ticker.assert_called_with("AAPL")
        self.assertTrue(mock_ticker_instance.history.called)

        # Verify that StockHistory entries were added
        self.assertEqual(self.mock_db_session.add.call_count, 2)  # Two records added
        self.mock_db_session.commit.assert_called_once()

    @patch("backend.market.yahoo_fetcher.Stock.query")
    def test_seed_database_if_empty(self, mock_stock_query):
        # Mock Stock query to simulate an empty database
        mock_stock_query.count.return_value = 0

        # Call the function
        seed_database_if_empty()

        # Verify that default stocks were added
        self.assertTrue(self.mock_db_session.add.called)
        self.mock_db_session.commit.assert_called_once()

if __name__ == "__main__":
    unittest.main()
