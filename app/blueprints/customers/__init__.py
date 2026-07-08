from flask import Blueprint

# = Customers blueprint:

# initialize blueprint:
customers_bp = Blueprint("customer_bp", __name__)

# import routes:
from . import routes