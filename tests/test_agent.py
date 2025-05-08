import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from flask import Flask
from flask_jwt_extended import create_access_token
from backend.models.user import User
from backend.extension import dbs as db
from backend.routes.agent import agent  # adjust if the import path is different
from unittest.mock import patch

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    db.init_app(app)

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

def test_list_customers_as_agent(client, app):
    with app.app_context():
        agent_user = create_user('agent', 'Agent Smith')
        customer1 = create_user('customer', 'John Doe')
        customer2 = create_user('customer', 'Jane Roe')

        access_token = create_access_token(identity=agent_user.id)

        response = client.get(
            "/api/customers",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["first_name"] == "John"
        assert data[1]["last_name"] == "Roe"

def test_list_customers_as_non_agent(client, app):
    with app.app_context():
        customer_user = create_user('customer', 'Eve Smith')
        access_token = create_access_token(identity=customer_user.id)

        response = client.get(
            "/api/customers",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        assert response.status_code == 403
        assert response.get_json() == {"error": "Access denied"}
