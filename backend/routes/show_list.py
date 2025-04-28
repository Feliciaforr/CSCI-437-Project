from flask import Blueprint, request, jsonify
from backend.extension import dbs as db
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import User, Transaction, Stock, Portfolio, StockCurrentprice
from backend.extension import dbs as db
from datetime import datetime


show_list = Blueprint("show_list", __name__)

@show_list.route('/show_list', methods=['GET'])
@jwt_required()
def list_stocks():
    stocks = Stock.query.all()
    stock_list = []

    for stock in stocks:
        current_price_entry = StockCurrentprice.query.filter_by(stock_id=stock.id).first()
        current_price = current_price_entry.price if current_price_entry else None

        stock_list.append({
            "symbol": stock.symbol,
            "name": stock.name,
            "current_price": current_price
        })

    return jsonify(stock_list), 200

@show_list.route('/stocks/today/<symbol>', methods=['GET'])
@jwt_required()
def get_today_prices(symbol):
    stock = Stock.query.filter_by(symbol=symbol).first()
    if not stock:
        return jsonify({"error": "Stock not found"}), 404

    from backend.models.stock_price_today import StockPriceToday
    intraday_entries = StockPriceToday.query.filter_by(stock_id=stock.id).order_by(StockPriceToday.time_stamp.asc()).all()

    data = [
        {"timestamp": entry.time_stamp.strftime('%Y-%m-%d %H:%M:%S'), "price": entry.price}
        for entry in intraday_entries
    ]

    return jsonify(data), 200

@show_list.route('/stocks/history/<symbol>', methods=['GET'])
@jwt_required()
def get_stock_history(symbol):
    range_param = request.args.get('range', '7d')
    valid_ranges = ['7d', '1m', '3m', '1y', '5y']
    if range_param not in valid_ranges:
        return jsonify({"error": "Invalid range parameter"}), 400

    stock = Stock.query.filter_by(symbol=symbol).first()
    if not stock:
        return jsonify({"error": "Stock not found"}), 404

    from backend.models.stock_history import StockHistory
    history_entries = StockHistory.query.filter_by(stock_id=stock.id).order_by(StockHistory.date.desc()).all()

    if range_param == '7d':
        history_entries = history_entries[:6]
    elif range_param == '1m':
        history_entries = history_entries[:29]
    elif range_param == '3m':
        history_entries = history_entries[:89]
    elif range_param == '1y':
        history_entries = history_entries[:364]
    elif range_param == '5y':
        history_entries = history_entries[:1824]

    data = [
        {"date": entry.date.isoformat(), "price": entry.average_price}
        for entry in history_entries
    ]

    return jsonify(data), 200