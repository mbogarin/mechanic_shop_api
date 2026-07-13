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
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return jsonify({"message": "You must be logged in to access this."}), 401
        
        auth_parts = auth_header.strip().split()
        
        # Accept "Bearer <token> or just <token>":
        
        if len(auth_parts) == 2 and auth_parts[0].lower() == "bearer":
            token = auth_parts[1]
            
        elif len(auth_parts) == 1:
            token = auth_parts[0]
        else:
            return jsonify({"message": "Invalid Authorization header"}), 401
            
        try:
            data = jwt.decode(
                token, 
                SECRET_KEY, 
                algorithms=["HS256"]
            ) # Decode token.
            
            customer_id = data["sub"] # Fetch customer ID.
            
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        
        except jose.exceptions.JWTError:
            return jsonify({"message": "Invalid Token."}), 401
    
        return f(customer_id, *args, **kwargs) 
                
    return decorated