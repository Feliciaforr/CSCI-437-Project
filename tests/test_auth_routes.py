import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash
from backend.models import User
from backend.extension import dbs as db
from backend.routes.auth_routes import auth

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret'
    db.init_app(app)
    JWTManager(app)

    with app.app_context():
        db.create_all()
        app.register_blueprint(auth, url_prefix='/api')
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_success(client):
    res = client.post('/api/register', json={
        'username': 'user1',
        'password': 'password123',
        'email': 'user1@example.com',
        'name': 'User One',
        'phone': '1234567890',
        'account_balance': 100.0,
        'role': 'customer'
    })
    assert res.status_code == 201
    assert res.get_json()['message'] == 'You did it Son'

def test_register_missing_fields(client):
    res = client.post('/api/register', json={'username': 'incomplete'})
    assert res.status_code == 400
    assert 'Missing required fields' in res.get_json()['error']

def test_register_duplicate_user(client, app):
    with app.app_context():
        user = User(username='dup', email='dup@example.com', password='hashed', name='Dup', phone='000', account_balance=0, role='customer')
        db.session.add(user)
        db.session.commit()
    res = client.post('/api/register', json={
        'username': 'dup',
        'password': 'password',
        'email': 'dup@example.com',
        'name': 'Dup Name',
        'phone': '111',
        'account_balance': 50.0,
        'role': 'customer'
    })
    assert res.status_code == 400
    assert 'Username or email already exists' in res.get_json()['error']

def test_login_success(client, app):
    with app.app_context():
        user = User(username='log', email='log@example.com', password=generate_password_hash('secret'), name='Log', phone='000', account_balance=0, role='customer')
        db.session.add(user)
        db.session.commit()
    res = client.post('/api/login', json={
        'email': 'log@example.com',
        'password': 'secret'
    })
    assert res.status_code == 200
    assert 'access_token' in res.get_json()

def test_login_wrong_password(client, app):
    with app.app_context():
        user = User(username='bad', email='bad@example.com', password=generate_password_hash('right'), name='Bad', phone='000', account_balance=0, role='customer')
        db.session.add(user)
        db.session.commit()
    res = client.post('/api/login', json={
        'email': 'bad@example.com',
        'password': 'wrong'
    })
    assert res.status_code == 401
    assert 'Invalid password' in res.get_json()['error']

def test_login_user_not_found(client):
    res = client.post('/api/login', json={
        'email': 'not@found.com',
        'password': 'anything'
    })
    assert res.status_code == 404
    assert 'User not found' in res.get_json()['error']

def test_login_missing_fields(client):
    res = client.post('/api/login', json={})
    assert res.status_code == 400
    assert 'Missing email or password' in res.get_json()['error']

def test_get_me_success(client, app):
    with app.app_context():
        user = User(username='me', email='me@example.com', password='pass', name='Me User', phone='000', account_balance=25.0, role='customer')
        db.session.add(user)
        db.session.commit()
        token = create_access_token(identity=user.id)
    res = client.get('/api/me', headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.get_json()['email'] == 'me@example.com'

def test_get_me_unauthenticated(client):
    res = client.get('/api/me')
    assert res.status_code == 401
    assert 'msg' in res.get_json()

def test_get_me_user_not_found(client, app):
    with app.app_context():
        # Create token for non-existent user id
        token = create_access_token(identity=999)
    res = client.get('/api/me', headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 404
    assert 'User not found' in res.get_json()['error']
