from flask import Blueprint, request, jsonify
from backend.extension import dbs as db
from flask_jwt_extended import jwt_required
from backend.models import  Stock, StockCurrentprice, StockHistory
from backend.extension import dbs as db
from datetime import datetime

suggestions = Blueprint("suggestions", __name__)


@suggestions.route("/suggestions", methods=["GET"])
@jwt_required()
def get_suggestions():
    stock_suggestions = []

    stocks = Stock.query.all()

    for stock in stocks:
        # Fetch last 20 historical closing prices
        history_entries = (
            StockHistory.query
            .filter_by(stock_id=stock.id)
            .order_by(StockHistory.date.desc())
            .limit(20)
            .all()
        )

        if len(history_entries) < 5:
            continue

        moving_average = sum(entry.average_price for entry in history_entries) / len(history_entries)

        # Fetch current live price
        current_entry = (
            StockCurrentprice.query
            .filter_by(stock_id=stock.id)
            .order_by(StockCurrentprice.timestamp.desc())
            .first()
        )

        if not current_entry:
            continue

        current_price = current_entry.price

        # Calculate % difference
        percent_diff = ((current_price - moving_average) / moving_average) * 100

        # Prepare suggestion item
        suggestion = {
            "symbol": stock.symbol,
            "name": stock.name,
            "current_price": round(current_price, 2),
            "moving_average": round(moving_average, 2),
            "percent_difference": round(percent_diff, 2),
            "suggestion": "BUY" if current_price < moving_average else "SELL"
        }

        stock_suggestions.append(suggestion)

    # Sort by absolute percent difference
    stock_suggestions.sort(key=lambda stock: abs(stock['percent_difference']), reverse=True)
    top_suggestions = stock_suggestions[:5]

    return jsonify(top_suggestions), 200