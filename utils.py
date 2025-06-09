from functools import wraps
from flask import jsonify, request

class APIError(Exception):
    """Custom exception for API errors."""
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

def validate_json_input(required_fields):
    """
    Decorator to validate if required JSON fields are present in the request body.
    Handles missing fields. 
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                raise APIError("Request must be JSON", status_code=400)
            data = request.get_json()
            for field in required_fields:
                if field not in data:
                    raise APIError(f"Missing required field: {field}", status_code=400)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def handle_api_error(e):
    """Error handler for APIError.""" 
    return jsonify({"error": e.message}), e.status_code

def is_valid_email(email):
    """Basic email format validation."""
    import re
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None