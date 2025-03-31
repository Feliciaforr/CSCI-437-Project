from flask import Blueprint

auth = Blueprint("auth",  __name__)

@auth.route('/login')
def login():
    return "Login works!"
# This is a simple Flask blueprint for authentication routes.
# It defines a route for user login that responds to POST requests.
# The route is registered with the blueprint named 'auth'.
# To use this blueprint, you would typically register it with a Flask application instance.
# For example:
# from flask import Flask
# from your_module import auth_routes