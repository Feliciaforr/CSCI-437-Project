from flask import Blueprint, request, jsonify
from backend.extension import dbs as db
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import User, Transaction, Stock, Portfolio, StockCurrentprice
from backend.extension import dbs as db
from datetime import datetime



trade = Blueprint("trade", __name__)

@trade.route('buy', methods=['POST'])
@jwt_required()
def buy_share():
    data = request.get_json()
    symbol = data.get('symbol')
    quantity = data.get('quantity')
    print(f"Buying {quantity} shares of {symbol}")
    if not symbol or not quantity:
        return jsonify({"error":"Missing symbol or quantity"}), 400
    
    user_id = get_jwt_identity()
    acting_customer_id = request.args.get('acting_customer_id')
    if acting_customer_id:
        user = User.query.get(user_id)
        if user.role != 'agent':
            return jsonify({"error": "Unauthorized impersonation attempt"}), 403
        user_id = acting_customer_id

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error":"User not found"}), 404
    
    stock = Stock.query.filter_by(symbol=symbol).first()
    stock_id = Stock.query.filter_by(symbol=symbol).first()
    print(f"Stock ID: {stock_id}")
    print(f"Stock found: {stock}")
    if not stock:
        return jsonify({"error":"Stock not found"}), 404
    
    print(f"Buying {quantity} shares of {symbol} for user {user_id}")
    current_price_entry = StockCurrentprice.query.filter_by(stock_id=stock.id).order_by(StockCurrentprice.timestamp.desc()).first()
    latest_price = current_price_entry.price if current_price_entry else None
    if not latest_price:
        return jsonify({"error":"Current price not found"}), 404
    
    total_cost = latest_price * quantity
    if user.account_balance < total_cost:
        return jsonify({"error":"Insufficient balance"}), 400
    
    # Deduct the cost from user's account balance
    user.account_balance -= total_cost
    
    portfolio = Portfolio.query.filter_by(user_id=user_id, stock_id=stock.id).first()
    
    if portfolio:
        total_quantity = portfolio.quantity + quantity
        total_investment = (portfolio.average_price * portfolio.quantity )+ total_cost
        portfolio.quantity = total_quantity
        portfolio.average_price = total_investment / total_quantity
    else:
        portfolio = Portfolio(
            user_id=user_id,
            stock_id=stock.id,
            quantity=quantity,
            average_price=latest_price
        )
        db.session.add(portfolio)
        
    # Create a transaction record
    transaction = Transaction(
        user_id=user_id,
        stock_id=stock.id,
        quantity=quantity,
        price=latest_price,
        transaction_type='buy'
        )
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify(
        {
            "message": "Stock purchased successfully",
            "stock": symbol,
            "quantity": quantity,
            "total_cost": total_cost,
            "remaining_balance": user.account_balance
        }
    ), 200

@trade.route('sell', methods=['POST'])
@jwt_required()
def sell_share():
    data = request.get_json()
    symbol = data.get('symbol')
    quantity = data.get('quantity')

    if not symbol or not quantity:
        return jsonify({"error": "Missing symbol or quantity"}), 400

    user_id = get_jwt_identity()
    acting_customer_id = request.args.get('acting_customer_id')
    if acting_customer_id:
        user = User.query.get(user_id)
        if user.role != 'agent':
            return jsonify({"error": "Unauthorized impersonation attempt"}), 403
        user_id = acting_customer_id

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    stock = Stock.query.filter_by(symbol=symbol).first()
    if not stock:
        return jsonify({"error": "Stock not found"}), 404

    current_price_entry = StockCurrentprice.query.filter_by(stock_id=stock.id).order_by(StockCurrentprice.timestamp.desc()).first()
    latest_price = current_price_entry.price if current_price_entry else None
    if not latest_price:
        return jsonify({"error": "Current price not found"}), 404

    portfolio = Portfolio.query.filter_by(user_id=user_id, stock_id=stock.id).first()
    if not portfolio or portfolio.quantity < quantity:
        return jsonify({"error": "Not enough shares to sell"}), 400

    # Calculate total proceeds and update user's balance
    total_earnings = latest_price * quantity
    user.account_balance += total_earnings

    # Update or remove portfolio entry
    portfolio.quantity -= quantity
    if portfolio.quantity == 0:
        db.session.delete(portfolio)

    # Record the transaction
    transaction = Transaction(
        user_id=user_id,
        stock_id=stock.id,
        quantity=quantity,
        price=latest_price,
        transaction_type='sell'
    )
    db.session.add(transaction)
    db.session.commit()

    return jsonify(
        {
            "message": "Stock sold successfully",
            "stock": symbol,
            "quantity": quantity,
            "total_earnings": total_earnings,
            "updated_balance": user.account_balance
        }
    ), 200

@trade.route('history', methods=['GET'])
@jwt_required()
def get_trade_history():
    user_id = get_jwt_identity()
    acting_customer_id = request.args.get('acting_customer_id')
    if acting_customer_id:
        user = User.query.get(user_id)
        if user.role != 'agent':
            return jsonify({"error": "Unauthorized impersonation attempt"}), 403
        user_id = acting_customer_id

    transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.timestamp.desc()).all()
    if not transactions:
        return jsonify({"message": "No trade history found"}), 404
    
    history = [
        {
            "stock": Stock.query.get(tx.stock_id).symbol,
            "transaction_type": tx.transaction_type,
            "quantity": tx.quantity,
            "price": tx.price,
            "timestamp": tx.timestamp.strftime("%Y-%m-%d %H:%M:%S") 
        }
        for tx in transactions
    ]
    return jsonify(history), 200

@trade.route('portfolio', methods=['GET'])
@jwt_required()
def get_portfolio():
    user_id = get_jwt_identity()
    acting_customer_id = request.args.get('acting_customer_id')
    if acting_customer_id:
        user = User.query.get(user_id)
        if user.role != 'agent':
            return jsonify({"error": "Unauthorized impersonation attempt"}), 403
        user_id = acting_customer_id

    portfolio_items = Portfolio.query.filter_by(user_id=user_id).all()

    if not portfolio_items:
        return jsonify({"message": "No portfolio data found"}), 404

    results = []
    for item in portfolio_items:
        stock = Stock.query.get(item.stock_id)
        current_price_entry = StockCurrentprice.query.filter_by(stock_id=stock.id).order_by(StockCurrentprice.timestamp.desc()).first()
        current_price = current_price_entry.price if current_price_entry else None
        if current_price is None:
            continue
        profit_or_loss = (current_price - item.average_price) * item.quantity
        results.append({
            "stock": stock.symbol,
            "quantity": item.quantity,
            "average_price": item.average_price,
            "current_price": current_price,
            "profit_or_loss": round(profit_or_loss, 2)
        })

    return jsonify(results), 200


