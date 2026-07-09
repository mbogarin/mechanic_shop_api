# Utility Functions:
from datetime import datetime, timedelta, timezone
from jose import jwt
import jose

from flask import request, jsonify
from functools import wraps


# = Token Authentication:

SECRET_KEY = "secret key"

# JWT Authentication:
def encode_token(customer_id):
    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(days=0, hours=1), # set expiration time.
        "iat": datetime.now(timezone.utc), # Issued date.
        "sub": str(customer_id), # String so token can be decoded.  
        
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


# TOKEN DECORATOR
def token_required(f):
    @wraps(f) # function wrapper.
    
    # Functionality:
    def decorated(*args, **kwargs):
        
        # Look for token in authorization header:
        if "Authorization" in request.headers:
            token = request.headers['Authorization'].split(" ")[1] # access token string.
            
            # If token is NOT found:
            if not token:
                return jsonify({"message" : "Token is missing!"}), 401
            
            # If token is found:
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"]) # Decode the token.
                customer_id = data['sub'] # Fetch customer ID.
                
                
            # Error messages:
            except jose.exceptions.ExpiredSignatureError:
                return jsonify({"message" : "Token has expired!"}), 401 # Expired token.
            
            except jose.exceptions.JWTError:
                return jsonify({"message" : "Invalid Token."}), 401 # Invalid token. 
            
        
            return f(customer_id, *args, **kwargs) # return wrapped function. 
                
        else:
            return jsonify({"message" : "You must be logged in to access this."}), 401
        
    return decorated