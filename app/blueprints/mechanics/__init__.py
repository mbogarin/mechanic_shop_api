from flask import Blueprint

# = Mechanics:

# Initialize blueprint:
mechanics_bp = Blueprint("mechanics_bp", __name__)

# Import routes:
from . import routes