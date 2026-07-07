from flask import Blueprint

# = Service Tickets:

# Initialize blueprint:
tickets_bp = Blueprint("tickets_bp", __name__)

# Import routes:
from . import routes