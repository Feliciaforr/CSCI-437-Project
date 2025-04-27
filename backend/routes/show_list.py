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