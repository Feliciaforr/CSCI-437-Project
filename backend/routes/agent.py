from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.extension import dbs as db
from backend.models.user import User
from backend.models import Transaction, Stock, Portfolio, StockCurrentprice

agent = Blueprint('agent', __name__)

@agent.route('/customers', methods=['GET'])
@jwt_required()
def list_customers():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user.role != 'agent':
        return jsonify({"error": "Access denied"}), 403

    customers = User.query.filter_by(role='customer').all()
    customers_data = [
        {
            "id": c.id,
            "first_name": c.name.split()[0],
            "last_name": c.name.split()[-1]
        }
        for c in customers
    ]
    return jsonify(customers_data), 200

@agent.route('/customer/<int:customer_id>/portfolio', methods=['GET'])
@jwt_required()
def agent_get_portfolio(customer_id):
    user_id = get_jwt_identity()
    agent_user = User.query.get(user_id)
    if agent_user.role != 'agent':
        return jsonify({"error": "Access denied"}), 403

    portfolio_items = Portfolio.query.filter_by(user_id=customer_id).all()
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

@agent.route('/customer/<int:customer_id>/buy', methods=['POST'])
@jwt_required()
def agent_buy_for_customer(customer_id):
    user_id = get_jwt_identity()
    agent_user = User.query.get(user_id)
    if agent_user.role != 'agent':
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json()
    symbol = data.get('symbol')
    quantity = data.get('quantity')
    if not symbol or not quantity:
        return jsonify({"error": "Missing symbol or quantity"}), 400

    user = User.query.get(customer_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    stock = Stock.query.filter_by(symbol=symbol).first()
    if not stock:
        return jsonify({"error": "Stock not found"}), 404

    current_price_entry = StockCurrentprice.query.filter_by(stock_id=stock.id).order_by(StockCurrentprice.timestamp.desc()).first()
    latest_price = current_price_entry.price if current_price_entry else None
    if not latest_price:
        return jsonify({"error": "Current price not found"}), 404

    total_cost = latest_price * quantity
    if user.account_balance < total_cost:
        return jsonify({"error": "Insufficient balance"}), 400

    user.account_balance -= total_cost
    portfolio = Portfolio.query.filter_by(user_id=customer_id, stock_id=stock.id).first()

    if portfolio:
        total_quantity = portfolio.quantity + quantity
        total_investment = (portfolio.average_price * portfolio.quantity) + total_cost
        portfolio.quantity = total_quantity
        portfolio.average_price = total_investment / total_quantity
    else:
        portfolio = Portfolio(
            user_id=customer_id,
            stock_id=stock.id,
            quantity=quantity,
            average_price=latest_price
        )
        db.session.add(portfolio)

    transaction = Transaction(
        user_id=customer_id,
        stock_id=stock.id,
        quantity=quantity,
        price=latest_price,
        transaction_type='buy'
    )
    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        "message": "Stock purchased successfully",
        "stock": symbol,
        "quantity": quantity,
        "total_cost": total_cost,
        "remaining_balance": user.account_balance
    }), 200

@agent.route('/customer/<int:customer_id>/sell', methods=['POST'])
@jwt_required()
def agent_sell_for_customer(customer_id):
    user_id = get_jwt_identity()
    agent_user = User.query.get(user_id)
    if agent_user.role != 'agent':
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json()
    symbol = data.get('symbol')
    quantity = data.get('quantity')
    if not symbol or not quantity:
        return jsonify({"error": "Missing symbol or quantity"}), 400

    user = User.query.get(customer_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    stock = Stock.query.filter_by(symbol=symbol).first()
    if not stock:
        return jsonify({"error": "Stock not found"}), 404

    current_price_entry = StockCurrentprice.query.filter_by(stock_id=stock.id).order_by(StockCurrentprice.timestamp.desc()).first()
    latest_price = current_price_entry.price if current_price_entry else None
    if not latest_price:
        return jsonify({"error": "Current price not found"}), 404

    portfolio = Portfolio.query.filter_by(user_id=customer_id, stock_id=stock.id).first()
    if not portfolio or portfolio.quantity < quantity:
        return jsonify({"error": "Not enough shares to sell"}), 400

    total_earnings = latest_price * quantity
    user.account_balance += total_earnings
    portfolio.quantity -= quantity
    if portfolio.quantity == 0:
        db.session.delete(portfolio)

    transaction = Transaction(
        user_id=customer_id,
        stock_id=stock.id,
        quantity=quantity,
        price=latest_price,
        transaction_type='sell'
    )
    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        "message": "Stock sold successfully",
        "stock": symbol,
        "quantity": quantity,
        "total_earnings": total_earnings,
        "updated_balance": user.account_balance
    }), 200



# Route for agent to get info for a specific customer by ID
@agent.route('/customer/<int:customer_id>/me', methods=['GET'])
@jwt_required()
def get_customer_info(customer_id):
    """
    Retrieves the specified customer's information (agent access).
    """
    user_id = get_jwt_identity()
    agent_user = User.query.get(user_id)
    if agent_user.role != 'agent':
        return jsonify({"error": "Access denied"}), 403

    user = User.query.get(customer_id)
    if not user:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "name": user.name,
        "account_balance": user.account_balance,
        "role": user.role
    }), 200