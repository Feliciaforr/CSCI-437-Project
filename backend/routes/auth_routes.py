from flask import Blueprint, request, jsonify
from extensiton import dbs as db
from models import User
from werkzeug.security import generate_password_hash

auth = Blueprint("auth",  __name__)

@auth.route('/login')
def login():
    
    return "Login works!"

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not all(key in data for key in ('username', 'password', 'email', 'name', 'phone', 'account_balance', "role")):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
        return jsonify({'error': 'Username or email already exists'}), 400
    
    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'],
        password=data['password'],  
        email=data['email'],
        name=data['name'],
        phone=data['phone'],
        role=data['role'],
        account_balance=data['account_balance']
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "You did it Son"}), 201
    
# This is a simple Flask blueprint for authentication routes.
# It defines a route for user login that responds to POST requests.
# The route is registered with the blueprint named 'auth'.
# To use this blueprint, you would typically register it with a Flask application instance.
# For example:
# from flask import Flask
# from your_module import auth_routes