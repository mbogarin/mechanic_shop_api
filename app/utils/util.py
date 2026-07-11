# Utility Functions:
from datetime import datetime, timedelta, timezone
from jose import jwt
import jose

from flask import request, jsonify
from functools import wraps


# Token Authentication:

SECRET_KEY = "secret key"

# JWT Authentication:
def encode_token(customer_id):
    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(days=0, hours=1), # Set expiration time.
        "iat": datetime.now(timezone.utc), # Issued date.
        "sub": str(customer_id), # Store customer id as string for decoding. 
        
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


# Token Decorator: require a valid customer JWT before running a protected route.
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
    
        if "Authorization" in request.headers:
            token = request.headers['Authorization'].split(" ")[1] 
            
            if not token:
                return jsonify({"message": "Token is missing!"}), 401
            
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"]) # Decode token.
                customer_id = data['sub'] # Fetch customer ID.
            except jose.exceptions.ExpiredSignatureError:
                return jsonify({"message": "Token has expired!"}), 401
            except jose.exceptions.JWTError:
                return jsonify({"message": "Invalid Token."}), 401
        
            return f(customer_id, *args, **kwargs) 
                
        else:
            return jsonify({"message": "You must be logged in to access this."}), 401
        
    return decorated