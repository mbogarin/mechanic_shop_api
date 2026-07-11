from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select

from app.utils.util import encode_token, token_required

from . import customers_bp
from .schemas import customer_schema, login_schema, paginated_customers_schema
from app.models import Customer, Service_Ticket, db
from app.blueprints.service_tickets.schemas import service_tickets_schema



# = CUSTOMER ROUTES:

# 1. (POST) CREATE CUSTOMER:
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


# 2 (POST): GET ALL CUSTOMERS:
@customers_bp.route("/", methods=["GET"])
def get_customers():
    
    # Pagination:
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)
    
    query = select(Customer)
    customers = db.paginate(query, page=page, per_page=per_page)
    
    return paginated_customers_schema.jsonify(customers), 200


# 3. (GET) GET SINGLE CUSTOMER:
@customers_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    
    if customer:
        return customer_schema.jsonify(customer), 200
    
    return jsonify({"error": "Customer not found."}), 404


# 4. (PUT) UPDATE SINGLE CUSTOMER: Protected route
@customers_bp.route("/", methods=["PUT"])
@token_required # authentication wrapper
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


# 5. (DELETE) DELETE SINGLE CUSTOMER: Protected route
@customers_bp.route("/", methods=["DELETE"])
@token_required # authentication wrapper
def delete_customer(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()
    
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    
    db.session.delete(customer)
    db.session.commit()
    
    return jsonify({"message": f"{customer.name} has been successfully deleted."}), 200


# = TOKEN AUTHENTICATION ROUTES:

# 6. (POST) LOGIN: Protected route
@customers_bp.route("/login", methods=["POST"])
def login(): 
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalars().first()

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
    
      
# 7. (GET) GET SERVICE TICKETS FOR AUTHORIZED CUSTOMER: protected route
@customers_bp.route("/my-tickets", methods=["GET"])
@token_required # Bearer token authentication
def get_my_tickets(customer_id):
    query = select(Service_Ticket).where(Service_Ticket.customer_id == customer_id)
    
    service_tickets = db.session.execute(query).scalars().all()
    
    return service_tickets_schema.jsonify(service_tickets), 200 