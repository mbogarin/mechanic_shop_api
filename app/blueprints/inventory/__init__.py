from flask import Blueprint

# = Inventory Blueprints:

# Initialize blueprint:
inventory_bp = Blueprint("inventory_bp", __name__)

# Import routes:
from . import routes