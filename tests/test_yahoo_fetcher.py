import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from backend.market.yahoo_fetcher import fetch_and_store_stock_data  # Replace with the actual function name

@pytest.fixture
def mock_db_session():
    with patch("backend.market.yahoo_fetcher.db.session") as mock_session:
        yield mock_session

@pytest.fixture
def mock_yfinance_ticker():
    with patch("backend.market.yahoo_fetcher.yf.Ticker") as mock_ticker:
        yield mock_ticker

def test_fetch_and_store_stock_data_success(mock_db_session, mock_yfinance_ticker):
    # Mock stock data from yfinance
    mock_ticker_instance = MagicMock()
    mock_ticker_instance.history.return_value = {
        "Open": [100.0],
        "Close": [110.0],
        "High": [115.0],
        "Low": [95.0],
        "Volume": [1000],
    }
    mock_yfinance_ticker.return_value = mock_ticker_instance

    # Call the function
    fetch_and_store_stock_data("AAPL")  # Replace with the actual function and arguments

    # Assertions
    mock_yfinance_ticker.assert_called_once_with("AAPL")
    mock_ticker_instance.history.assert_called_once()
    assert mock_db_session.add.call_count > 0  # Ensure data is added to the database
    mock_db_session.commit.assert_called_once()

def test_fetch_and_store_stock_data_no_data(mock_db_session, mock_yfinance_ticker):
    # Mock yfinance to return no data
    mock_ticker_instance = MagicMock()
    mock_ticker_instance.history.return_value = {}
    mock_yfinance_ticker.return_value = mock_ticker_instance

    # Call the function
    fetch_and_store_stock_data("AAPL")  # Replace with the actual function and arguments

    # Assertions
    mock_yfinance_ticker.assert_called_once_with("AAPL")
    mock_ticker_instance.history.assert_called_once()
    mock_db_session.add.assert_not_called()  # No data should be added to the database
    mock_db_session.commit.assert_not_called()

def test_fetch_and_store_stock_data_db_error(mock_db_session, mock_yfinance_ticker):
    # Mock stock data from yfinance
    mock_ticker_instance = MagicMock()
    mock_ticker_instance.history.return_value = {
        "Open": [100.0],
        "Close": [110.0],
        "High": [115.0],
        "Low": [95.0],
        "Volume": [1000],
    }
    mock_yfinance_ticker.return_value = mock_ticker_instance

    # Simulate a database error
    mock_db_session.commit.side_effect = Exception("Database error")

    # Call the function and expect an exception
    with pytest.raises(Exception, match="Database error"):
        fetch_and_store_stock_data("AAPL")  # Replace with the actual function and arguments

    # Assertions
    mock_yfinance_ticker.assert_called_once_with("AAPL")
    mock_ticker_instance.history.assert_called_once()
    mock_db_session.add.assert_called()  # Data should still be added before the error