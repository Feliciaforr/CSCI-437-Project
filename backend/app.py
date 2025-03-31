from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from routes.auth_routes import auth


# Initialize Flask application
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

CORS(app)

# Initialize SQLAlchemy
db = SQLAlchemy()


# Configure database URI



app.register_blueprint(auth, url_prefix='/auth')
@app.route('/')
def hello_world():
    return 'Hello, World!'





if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=9000)
# This is a simple Flask application that returns "Hello, World!" when accessed at the root URL.
# The application is set to run in debug mode, which is useful for development.
# To run this application, save it as app.py and execute it with Python.
# Make sure to have Flask installed in your Python environment.
# You can install Flask using pip:
# pip install Flask
# After installing Flask, run the application with:
# python app.py