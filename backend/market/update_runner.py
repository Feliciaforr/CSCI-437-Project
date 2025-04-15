import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import time
from backend.market.finnhub_fetcher import fetch_and_store_intraday_data, update_current_prices_only



if __name__ == "__main__":
    print("Running full intraday data fetch once...")
    fetch_and_store_intraday_data()

    print("Starting live updates every 20 seconds...")
    while True:
        update_current_prices_only()
        time.sleep(20)
        