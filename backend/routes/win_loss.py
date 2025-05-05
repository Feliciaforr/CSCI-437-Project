from flask import Blueprint, jsonify
from backend.extension import dbs as db
from backend.models import Stock, StockPriceToday, StockCurrentprice, StockHistory
from flask_jwt_extended import jwt_required
from datetime import datetime

win_loss = Blueprint('win_loss', __name__)

def calculate_stock_changes():
    stock_changes = []

    stocks = Stock.query.all()

    for stock in stocks:
        yesterday_history = (
            StockHistory.query
            .filter(StockHistory.stock_id == stock.id)
            .order_by(StockHistory.date.desc())
            .first()
        )

        if not yesterday_history:
            continue

        current_entry = (
            StockCurrentprice.query
            .filter_by(stock_id=stock.id)
            .order_by(StockCurrentprice.timestamp.desc())
            .first()
        )

        if not current_entry:
            continue

        opening_price = yesterday_history.average_price
        current_price = current_entry.price

        if opening_price == 0:
            continue

        percent_change = ((current_price - opening_price) / opening_price) * 100

        stock_changes.append({
            "symbol": stock.symbol,
            "name": stock.name,
            "current_price": round(current_price, 2),
            "percent_change": round(percent_change, 2)
        })

    return stock_changes

@win_loss.route('/gainers', methods=['GET'])
@jwt_required()
def get_gainers():
    changes = calculate_stock_changes()
    gainers = sorted([s for s in changes if s['percent_change'] > 0], key=lambda x: x['percent_change'], reverse=True)[:6]
    return jsonify(gainers), 200

@win_loss.route('/losers', methods=['GET'])
@jwt_required()
def get_losers():
    changes = calculate_stock_changes()
    losers = sorted([s for s in changes if s['percent_change'] < 0], key=lambda x: x['percent_change'])[:6]
    return jsonify(losers), 200
