from flask import jsonify
from flask_jwt_extended import get_jwt

def require_role(requred_role):
    """
    Decorator to require a specific role for accessing a route.
    """
    claims = get_jwt()
    user_role = claims.get('role')
    if user_role != requred_role:
        return jsonify({"msg": f"Access denied. Reruired role: {require_role}"}), 403
    return None