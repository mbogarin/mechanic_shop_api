# Utility Functions:

# = Token Authentication:

from datetime import datetime, timedelta, timezone
from jose import jwt


SECRET_KEY = "secret key"

def encode_token(customer_id):
    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(days=0, hours=1), # set expiration time.
        "iat": datetime.now(timezone.utc), # Issued date.
        "sub": str(customer_id), # String so token can be decoded.  
        
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

