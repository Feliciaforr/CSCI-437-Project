import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from backend.models.user import User
from backend.extension import dbs as db
from backend.routes.agent import agent

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
        app.register_blueprint(agent, url_prefix="/api")
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def create_user(role, name):
    user = User(name=name, role=role)
    db.session.add(user)
    db.session.commit()
    return user

def test_customers_valid_agent(client, app):
    with app.app_context():
        agent = create_user('agent', 'Agent Smith')
        create_user('customer', 'John Doe')
        create_user('customer', 'Jane Roe')
        token = create_access_token(identity=agent.id)

        res = client.get('/api/customers', headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 200
        data = res.get_json()
        assert isinstance(data, list)
        assert len(data) == 2

def test_customers_non_agent(client, app):
    with app.app_context():
        customer = create_user('customer', 'Eve Adams')
        token = create_access_token(identity=customer.id)

        res = client.get('/api/customers', headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 403
        assert res.get_json() == {"error": "Access denied"}

def test_customers_no_token(client):
    res = client.get('/api/customers')
    assert res.status_code == 401
    assert "msg" in res.get_json()

def test_customers_malformed_token(client):
    res = client.get('/api/customers', headers={"Authorization": "Bearer invalidtoken"})
    assert res.status_code in (422, 401)  # Depending on JWT version
    assert "msg" in res.get_json()

def test_customers_empty_list(client, app):
    with app.app_context():
        agent = create_user('agent', 'Agent Zero')
        token = create_access_token(identity=agent.id)

        res = client.get('/api/customers', headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 200
        assert res.get_json() == []
