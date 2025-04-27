from flask import Blueprint, request, jsonify, session
from backend.extension import dbs as db
from backend.models import User, Alert, StockCurrentprice
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

alert = Blueprint("alert", __name__)

@alert.route('/notification', methods=['GET'])
@jwt_required()
def get_alerts():
    alerts = Alert.query.order_by(Alert.triggered_at.desc()).all()
    alert_list = []
    for a in alerts:
        alert_list.append({
            "stock_symbol": a.stock.symbol,
            "stock_name": a.stock.name,
            "change_percentage": a.change_percentage,
            "direction": a.direction,
            "triggered_at":  a.triggered_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(alert_list), 200