from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.extension import dbs as db
from backend.models.user import User

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