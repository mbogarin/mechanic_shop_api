from flask import Flask
from .extensions import ma
from .models import db
from .blueprints.customers import customers_bp
from .blueprints.mechanics import mechanics_bp

# Initializes Flask app & returns it:
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    
    
    # Initialize extensions:
    ma.init_app(app)
    db.init_app(app)
    
    # Register blueprints:
    
    # 1. Customer:
    app.register_blueprint(customers_bp, url_prefix='/customers') # - note: remove url prefix from CRUD operations. 
    
    
    # 2. Mechanic:
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    
    
    return app