from flask import Blueprint

# = Customers Blueprint:

# initialize blueprint:
customers_bp = Blueprint("customer_bp", __name__)

# import routes:
from . import routes