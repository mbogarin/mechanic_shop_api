from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select

from .schemas import service_ticket_schema, service_tickets_schema, edit_ticket_schema, return_ticket_schema
from app.models import db, Service_Ticket, Customer, Mechanic, Inventory
from . import service_tickets_bp

from app.extensions import limiter, cache


# = SERVICE TICKET ROUTES:
# 1. (POST): CREATE NEW SERVICE TICKET
@service_tickets_bp.route("/", methods=["POST"])
def create_service_ticket():
    try:
        ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    customer = db.session.get(Customer, ticket_data["customer_id"])
    
    if not customer: 
        return jsonify({"error": "Customer not found."}), 404
    
    # Prevent duplicate VINs since VIN must be unique in the database:
    query = select(Service_Ticket).where(Service_Ticket.VIN == ticket_data["VIN"])
    existing_ticket = db.session.execute(query).scalars().first()
    
    if existing_ticket:
        return jsonify({"error": "VIN is already associated with another service ticket."}), 400
    
    new_ticket = Service_Ticket(**ticket_data)
    db.session.add(new_ticket)
    db.session.commit()
    
    return service_ticket_schema.jsonify(new_ticket), 201



# 2. (GET): GET ALL SERVICE TICKETS
@service_tickets_bp.route("/", methods=["GET"])
@cache.cached(timeout=60) # Cache service ticket list for faster repeated GET requests.
def get_service_tickets():
    query = select(Service_Ticket)
    tickets = db.session.execute(query).scalars().all()
    
    return service_tickets_schema.jsonify(tickets), 200



# Many-to-Many relationship: Service ticket & Mechanic

# 3. (PUT): ASSIGN MECHANIC TO SERVICE TICKET
@service_tickets_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=["PUT"])
@limiter.limit("5 per hour") # Limit repeated mechanic assignment requests.
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(Service_Ticket, ticket_id)
    if not ticket: 
        return jsonify({"error": "Service ticket not found."}), 404
    

    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    # Check if the mechanic is already assigned to this service ticket:
    if mechanic in ticket.mechanics:
        return jsonify({"message":"Mechanic is already assigned to this service ticket."}), 200
    
    # Assign the mechanic to the service ticket:
    ticket.mechanics.append(mechanic) # mechanics list
    db.session.commit()
    cache.clear()
        
    return service_ticket_schema.jsonify(ticket), 200
    
    

# 4. (PUT): REMOVE MECHANIC FROM SERVICE TICKET
@service_tickets_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=["PUT"])
def remove_mechanic(ticket_id, mechanic_id):
    
 
    ticket = db.session.get(Service_Ticket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    

    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    # Check if the mechanic is not already assigned to this service ticket:
    if mechanic not in ticket.mechanics:
        return jsonify({"message": f"Mechanic {mechanic.name} is not assigned to this service ticket."}), 200
    
    # Remove the mechanic from the service ticket:
    ticket.mechanics.remove(mechanic) # mechanics list
    db.session.commit()
    cache.clear()
        
    return service_ticket_schema.jsonify(ticket), 200


# 5. (PUT): EDIT SERVICE TICKET
@service_tickets_bp.route("/<int:ticket_id>/edit", methods=['PUT'])
def edit_ticket(ticket_id):
    try:
        ticket_edits = edit_ticket_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    if not isinstance(ticket_edits, dict):
        return jsonify({"error": "Invalid request data."}), 400
    
    query = select(Service_Ticket).where(Service_Ticket.id == ticket_id)
    ticket = db.session.execute(query).scalars().first()
    
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    
            
    # ADD mechanics to a service ticket:
    for mechanic_id in ticket_edits.get("add_ids", []):
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()
        
        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)
            
    
    # REMOVE mechanics from a service ticket:
    for mechanic_id in ticket_edits.get("remove_ids", []):
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()
        
        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)

    
    db.session.commit()
    cache.clear() # clear caching so requests show updated data. 
    
    return return_ticket_schema.jsonify(ticket), 200



# 6. (PUT): ADD INVENTORY PART TO SERVICE TICKET
@service_tickets_bp.route("/<int:ticket_id>/add-part/<int:part_id>", methods=["PUT"])
def add_part_to_ticket(ticket_id, part_id):
    ticket = db.session.get(Service_Ticket, ticket_id)
    part = db.session.get(Inventory, part_id)
    
    if not ticket:
        return jsonify({"message": "Service ticket not found."}), 404
    
    if not part: 
        return jsonify({"message": "Inventory part not found."}), 404
    
    if part in ticket.parts:
        return jsonify({"message": f"{part.name} is already added to this service ticket."}), 400
    
    ticket.parts.append(part)
    db.session.commit()
    cache.clear()
    
    return service_ticket_schema.jsonify(ticket), 200
    
    
    

    


