from flask import Blueprint

# = Inventory blueprint:

# initialize blueprint:
inventory_bp = Blueprint("inventory_bp", __name__)

# import routes:
from . import routes