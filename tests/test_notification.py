import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv()
import pytest
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from backend.models import User, Alert, StockCurrentprice
from backend.extension import dbs as db
from backend.routes.alerts_notfications import alert
from datetime import datetime

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['FLASK_ENV'] = os.getenv('FLASK_ENV')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # Configure database connection
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    db_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.init_app(app)
    JWTManager(app)

    with app.app_context():
        db.create_all()
        app.register_blueprint(alert, url_prefix='/api')
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def create_user():
    user = User(
        username='testuser',
        email='test@example.com',
        password='test123',  # add hashing if needed
        name='Test User',
        role='customer',
        is_active=True
    )
    db.session.add(user)
    db.session.commit()
    return user

def create_stock():
    stock = StockCurrentprice(symbol='AAPL', name='Apple Inc.')
    db.session.add(stock)
    db.session.commit()
    return stock

def create_alert(stock, user):
    alert = Alert(
        stock_id=stock.id,
        user_id=user.id,
        change_percentage=2.5,
        direction='up',
        triggered_at=datetime(2024, 5, 1, 15, 30, 0)
    )
    db.session.add(alert)
    db.session.commit()
    return alert

def test_get_alerts_success(client, app):
    with app.app_context():
        user = create_user()
        stock = create_stock()
        create_alert(stock, user)
        token = create_access_token(identity=user.id)

        res = client.get('/api/notification', headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 200
        data = res.get_json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]['stock_symbol'] == 'AAPL'
        assert data[0]['stock_name'] == 'Apple Inc.'
        assert data[0]['direction'] == 'up'
        assert data[0]['change_percentage'] == 2.5
        assert data[0]['triggered_at'] == "2024-05-01 15:30:00"

def test_get_alerts_unauthenticated(client):
    res = client.get('/api/notification')
    assert res.status_code == 401
    assert "msg" in res.get_json()

def test_get_alerts_empty(client, app):
    with app.app_context():
        user = create_user()
        token = create_access_token(identity=user.id)
        res = client.get('/api/notification', headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 200
        data = res.get_json()
        assert data == []