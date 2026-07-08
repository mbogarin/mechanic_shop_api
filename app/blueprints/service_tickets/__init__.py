from flask import Blueprint

# = Service Tickets blueprint:

# Initialize blueprint:
service_tickets_bp = Blueprint("service_tickets_bp", __name__)

# Import routes:
from . import routes