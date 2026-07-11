from flask import Blueprint

# = Service Tickets Blueprint:

# Initialize blueprint:
service_tickets_bp = Blueprint("service_tickets_bp", __name__)

# Import routes:
from . import routes