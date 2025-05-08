import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch

# Assuming update_runner.py calls functions from finnhub_fetcher
from backend.market.update_runner import main  # Replace `main` with the actual function in update_runner

@patch("backend.market.finnhub_fetcher.fetch_and_store_intraday_data")
@patch("backend.market.finnhub_fetcher.update_current_prices_only")
def test_update_runner_calls_functions(mock_update_prices, mock_fetch_data):
    # Call the main function (or equivalent) in update_runner
    main()

    # Assert that the functions from finnhub_fetcher were called
    mock_fetch_data.assert_called_once()
    mock_update_prices.assert_called_once()

@patch("backend.market.finnhub_fetcher.fetch_and_store_intraday_data")
@patch("backend.market.finnhub_fetcher.update_current_prices_only")
def test_update_runner_handles_exceptions(mock_update_prices, mock_fetch_data):
    # Simulate an exception in one of the functions
    mock_fetch_data.side_effect = Exception("API error")

    # Call the main function (or equivalent) in update_runner
    with pytest.raises(Exception, match="API error"):
        main()

    # Ensure the second function is not called after the exception
    mock_update_prices.assert_not_called()
    