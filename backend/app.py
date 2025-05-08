import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
import os
# from routes.auth_routes import auth
from backend.routes.auth_routes import auth
from backend.routes.trade import trade
from backend.routes.alerts_notfications import alert
from backend.routes.suggestions import suggestions
from backend.routes.win_loss import win_loss
from backend.routes.agent import agent
from backend.routes.show_list import show_list
import sys
from backend.models import User, Stock, Portfolio, Transaction, Alert, StockPriceToday, StockCurrentprice, StockHistory
from backend.extension import dbs
from flask_jwt_extended import JWTManager


# Initialize Flask application
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

CORS(app)
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
# Configure database URI
db_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri



jwt = JWTManager(app)
dbs.init_app(app)


# Configure database URI



app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(trade, url_prefix='/trade')
app.register_blueprint(alert,url_prefix='/alert')
app.register_blueprint(suggestions,url_prefix='/suggest')
app.register_blueprint(win_loss,url_prefix='/win_loss')
app.register_blueprint(agent,url_prefix='/agent')
app.register_blueprint(show_list,url_prefix='/fetch')
@app.route('/')
def hello_world():
    return 'Hello, World!'





if __name__ == '__main__':
    with app.app_context():
        dbs.create_all()  
    app.run(host='0.0.0.0',debug=True, port=9000)
