from flask import Blueprint

customers_bp = Blueprint("customer_bp", __name__)

from . import routes