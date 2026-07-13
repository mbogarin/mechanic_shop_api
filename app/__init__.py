from flask import Flask,jsonify
from .extensions import ma, limiter, cache
from .models import db

from .blueprints.customers import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import service_tickets_bp
from .blueprints.inventory import inventory_bp

from flask_swagger_ui import get_swaggerui_blueprint
from flask_swagger import swagger
import yaml

# Swagger setup:
SWAGGER_URL = "/api/docs"  # URL for exposing Swagger UI
API_URL = "/api/swagger.json"  # API URL 

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Mechanic Shop API"
    }
)

# Create & configure the Flask app:
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    
    
    # Initialize extensions:
    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app) # Flask-Limiter
    cache.init_app(app) # Flask-Caching
    
    # Global 429 error handler for rate-limited endpoints:
    @app.errorhandler(429)
    def ratelimit_handler(error):
        return {
            "error": "Too Many Requests",
            "message": error.description
        }, 429
    
    # Add JSON specification route for Swagger UI
    @app.route("/api/swagger.json")
    
    def swagger_spec():
        with app.open_resource("static/swagger.yaml") as swagger_file:
            swagger_template = yaml.safe_load(swagger_file)
            
        
        return jsonify(
            swagger(app, template=swagger_template)
        )
        
    
    # Register blueprints:
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service-tickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL) # Swagger blueprint.
    
    

    return app