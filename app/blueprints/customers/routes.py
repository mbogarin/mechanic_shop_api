# CUSTOMER ROUTES:

from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select

from .schemas import customer_schema, customers_schema, login_schema
from app.models import Customer, db
from . import customers_bp

from app.utils.util import encode_token # Token authentication



# = Login route (Token Authentication):
@customers_bp.route("/login", methods=["POST"])
def login():
    
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalars().first() # Query for customer w/ matching email. 

    # If customer w/ matching email is found, validate password:
    if customer and customer.password == password:
        token = encode_token(customer.id)
        
        response = {
            "status" : "success",
            "message" : "Customer successfully logged in!",
            "token" : token
        }
        
        return jsonify(response), 200
    else:
        return jsonify({"message": 'Invalid email or password! Please try again.'}), 401



# = 1. Create new customer (POST):
@customers_bp.route('/', methods=['POST'])
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == customer_data["email"])
    existing_customer = db.session.execute(query).scalars().all()
    
    if existing_customer:
        return jsonify({"message": "Email is already associated with an account."}), 400
    
    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201


# = 2. Retrieve all customers (GET):
@customers_bp.route("/", methods=["GET"])
def get_customers():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    
    return customers_schema.jsonify(customers), 200


# = 3. Retrieve specific customer (GET):
@customers_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    
    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"error": "Customer not found."}), 404


# = 4. Update specific customer (PUT):
@customers_bp.route("/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    
    try:
        updated_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in updated_data.items():
        setattr(customer, key, value)
    
    db.session.commit()
    return customer_schema.jsonify(customer), 200


# = 5. Delete specific customer (DELETE):
@customers_bp.route("/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer id: {customer_id}, successfully deleted."}), 200