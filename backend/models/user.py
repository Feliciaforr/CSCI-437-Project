from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from extensiton import dbs as db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    account_balance = db.Column(db.Float, default=0.0)
    name = db.Column(db.String(80), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    role = db.Column(db.String(20), nullable=False, default="customer")
    
    
    """User model for authentication and profile management.

    Stores user credentials, contact details, and status. Tracks creation and update timestamps.

    Fields:
    - `username`: unique identifier for the user.
    - `email`: unique email address.
    - `password`: securely hashed password.
    - `name`: optional full name.
    - `phone`: optional contact number.
    -`account_balance`: user's account balance, defaults to 0.0.
    - `is_active`: soft-deletion flag (active/inactive).
    - `created_at`: timestamp for record creation.
    - `updated_at`: auto-updated timestamp for modifications.
    """
