import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from datetime import datetime
from backend.models import Alert, StockCurrentprice, Stock, StockPriceToday, StockHistory
from backend.extension import dbs as db
from backend.app import app
import time, math

INTERVAL = 2 #subject to change

def start_alert_checks():
    with app.app_context():
        baseline_prices = {}  
        last_alert_steps = {}  

        stocks = Stock.query.all()
        for stock in stocks:
            last_history_entry = StockHistory.query.filter_by(stock_id=stock.id).order_by(StockHistory.date.desc()).first()
            if last_history_entry:
                baseline_prices[stock.id] = last_history_entry.average_price
                print(f"Baseline price for {stock.symbol} from {last_history_entry.date} is {last_history_entry.average_price}")
                last_alert_steps[stock.id] = {"up": 0, "down": 0}
            else:
                print(f"No baseline history for {stock.symbol}")

        while True:
            for stock in stocks:
                latest_price_entry = StockPriceToday.query.filter_by(stock_id=stock.id).order_by(StockPriceToday.time_stamp.desc()).first()
                if not latest_price_entry:
                    continue

                current_price = latest_price_entry.price
                baseline_price = baseline_prices.get(stock.id)
                print("baseline_price", baseline_price)
                print("current_price", current_price)

                if not baseline_price or not current_price:
                    continue

                percent_change = ((current_price - baseline_price) / baseline_price) * 100

                if percent_change >= last_alert_steps[stock.id]["up"] + INTERVAL:
                    new_step = math.floor(percent_change / INTERVAL) * INTERVAL
                    last_alert_steps[stock.id]["up"] = new_step
                    print(f"{stock.symbol} moved UP by {round(percent_change, 2)}%")
                    create_alert(stock.id, percent_change, 'up')

                if percent_change <= -(last_alert_steps[stock.id]["down"] + INTERVAL):
                    new_step = math.floor(abs(percent_change) / INTERVAL) * INTERVAL
                    last_alert_steps[stock.id]["down"] = new_step
                    print(f"{stock.symbol} moved DOWN by {round(percent_change, 2)}%")
                    create_alert(stock.id, percent_change, 'down')

            time.sleep(60)  

def create_alert(stock_id, percent_change, direction):
    with app.app_context():
        new_alert = Alert(
            stock_id=stock_id,
            change_percentage=round(percent_change, 2),
            direction=direction,
            triggered_at=datetime.now()
        )
        db.session.add(new_alert)
        db.session.commit()