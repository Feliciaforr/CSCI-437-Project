from flask import Blueprint, request, jsonify, session
from backend.extension import dbs as db
from backend.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# Blueprint for authentication-related routes
auth = Blueprint("auth", __name__)

@auth.route('/login', methods=['POST'])
def login():
    """
    Handles user login by validating credentials.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Ensure both email and password are provided
    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400
    
    # Check if the user exists
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Verify the provided password
    if not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid password'}), 401
    
    #Gernerate JWT token for the user
    additional_claims = {"role": user.role}
    access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
   

    # Return user details on successful login
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'name': user.name,
            'account_balance': user.account_balance,
            "role": user.role
        }
    }), 200

@auth.route('/register', methods=['POST'])
def register():
    """
    Handles user registration by creating a new user. 
    """
    data = request.get_json()
    
    # Ensure all required fields are provided
    required_fields = ('username', 'password', 'email', 'name', 'phone', 'account_balance', "role")
    if not all(key in data for key in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if the username or email already exists
    if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
        return jsonify({'error': 'Username or email already exists'}), 400
    
    # Hash the password for security
    hashed_password = generate_password_hash(data['password'])
    
    # Create a new user instance
    new_user = User(
        username=data['username'],
        password=hashed_password,  
        email=data['email'],
        name=data['name'],
        phone=data['phone'],
        role=data['role'],
        account_balance=data['account_balance']
    )
    
    # Save the new user to the database
    db.session.add(new_user)
    db.session.commit()
    
    # Return a success message
    return jsonify({"message": "You did it Son"}), 201


@auth.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Retrieves the current user's information.
    """
    user_id = get_jwt_identity()
    
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "name": user.name,
        "account_balance": user.account_balance,
        "role": user.role
    }), 200

# This file defines routes for user authentication, including login and registration.
# The routes are part of the 'auth' blueprint, which can be registered with a Flask app.