import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from backend.market.finnhub_fetcher import fetch_and_store_intraday_data, update_current_prices_only

# FILE: backend/market/test_finnhub_fetcher.py

@pytest.fixture
def mock_db_session():
    with patch("..finnhub_fetcher.db.session") as mock_session:
        yield mock_session

@pytest.fixture
def mock_yfinance_ticker():
    with patch("..finnhub_fetcher.yf.Ticker") as mock_ticker:
        yield mock_ticker

@pytest.fixture
def mock_requests_get():
    with patch("..finnhub_fetcher.requests.get") as mock_get:
        yield mock_get

def test_fetch_and_store_intraday_data_success(mock_db_session, mock_yfinance_ticker):
    # Mock database query to return a list of stocks
    mock_stock = MagicMock()
    mock_stock.id = 1
    mock_stock.symbol = "AAPL"
    mock_db_session.query.return_value.all.return_value = [mock_stock]

    # Mock Yahoo Finance API response
    mock_ticker_instance = MagicMock()
    mock_data = MagicMock()
    mock_data.empty = False
    mock_data.iterrows.return_value = [
        (datetime(2023, 10, 1, 9, 30), {"High": 150, "Low": 145}),
        (datetime(2023, 10, 1, 9, 35), {"High": 152, "Low": 148}),
    ]
    mock_data.iloc[-1] = {"High": 152, "Low": 148}
    mock_ticker_instance.history.return_value = mock_data
    mock_yfinance_ticker.return_value = mock_ticker_instance

    # Call the function
    fetch_and_store_intraday_data()

    # Assertions
    mock_yfinance_ticker.assert_called_once_with("AAPL")
    assert mock_db_session.add.call_count == 3  # 2 intraday records + 1 current price
    mock_db_session.commit.assert_called_once()

def test_update_current_prices_only_success(mock_db_session, mock_requests_get):
    # Mock database query to return a list of stocks
    mock_stock = MagicMock()
    mock_stock.id = 1
    mock_stock.symbol = "AAPL"
    mock_db_session.query.return_value.all.return_value = [mock_stock]

    # Mock Finnhub API response
    mock_response = MagicMock()
    mock_response.json.return_value = {"c": 150.0}
    mock_requests_get.return_value = mock_response

    # Call the function
    update_current_prices_only()

    # Assertions
    mock_requests_get.assert_called_once_with(
        "https://finnhub.io/api/v1/quote",
        params={"symbol": "AAPL", "token": None}
    )
    assert mock_db_session.add.call_count == 2  # 1 current price + 1 price today
    mock_db_session.commit.assert_called_once()

def test_update_current_prices_only_no_data(mock_db_session, mock_requests_get):
    # Mock database query to return a list of stocks
    mock_stock = MagicMock()
    mock_stock.id = 1
    mock_stock.symbol = "AAPL"
    mock_db_session.query.return_value.all.return_value = [mock_stock]

    # Mock Finnhub API response with no data
    mock_response = MagicMock()
    mock_response.json.return_value = {}
    mock_requests_get.return_value = mock_response

    # Call the function
    update_current_prices_only()

    # Assertions
    mock_requests_get.assert_called_once_with(
        "https://finnhub.io/api/v1/quote",
        params={"symbol": "AAPL", "token": None}
    )
    assert mock_db_session.add.call_count == 0  # No data added
    mock_db_session.commit.assert_called_once()
    import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from backend.market.finnhub_fetcher import update_current_prices_only

# FILE: backend/market/test_finnhub_fetcher.py

@pytest.fixture
def mock_db_session():
    with patch("..finnhub_fetcher.db.session") as mock_session:
        yield mock_session

@pytest.fixture
def mock_requests_get():
    with patch("..finnhub_fetcher.requests.get") as mock_get:
        yield mock_get

def test_update_current_prices_only_success(mock_db_session, mock_requests_get):
    # Mock database query to return a list of stocks
    mock_stock = MagicMock()
    mock_stock.id = 1
    mock_stock.symbol = "AAPL"
    mock_db_session.query.return_value.all.return_value = [mock_stock]

    # Mock API response with valid data
    mock_response = MagicMock()
    mock_response.json.return_value = {"c": 150.0}
    mock_requests_get.return_value = mock_response

    # Call the function
    update_current_prices_only()

    # Assertions
    mock_requests_get.assert_called_once_with(
        "https://finnhub.io/api/v1/quote",
        params={"symbol": "AAPL", "token": None}
    )
    assert mock_db_session.add.call_count == 2  # One for StockCurrentprice, one for StockPriceToday
    mock_db_session.commit.assert_called_once()

def test_update_current_prices_only_no_data(mock_db_session, mock_requests_get):
    # Mock database query to return a list of stocks
    mock_stock = MagicMock()
    mock_stock.id = 1
    mock_stock.symbol = "AAPL"
    mock_db_session.query.return_value.all.return_value = [mock_stock]

    # Mock API response with no data
    mock_response = MagicMock()
    mock_response.json.return_value = {}
    mock_requests_get.return_value = mock_response

    # Call the function
    update_current_prices_only()

    # Assertions
    mock_requests_get.assert_called_once_with(
        "https://finnhub.io/api/v1/quote",
        params={"symbol": "AAPL", "token": None}
    )
    assert mock_db_session.add.call_count == 0  # No data added
    mock_db_session.commit.assert_called_once()