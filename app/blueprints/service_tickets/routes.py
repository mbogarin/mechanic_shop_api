from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select

from .schemas import service_ticket_schema, service_tickets_schema
from app.models import Service_Ticket, Customer, Mechanic, db
from . import service_tickets_bp


# SERVICE TICKET ROUTES:

# = 1. Create new service ticket (POST):
@service_tickets_bp.route("/", methods=["POST"])
def create_service_ticket():
    try:
        ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # Check if customer exists:
    customer = db.session.get(Customer, ticket_data["customer_id"])
    if not customer: 
        return jsonify({"error": "Customer not found."}), 404
    
    new_ticket = Service_Ticket(**ticket_data)
    db.session.add(new_ticket)
    db.session.commit()
    
    return service_ticket_schema.jsonify(new_ticket), 201



# = 2. Retrieve all service tickets (GET):
@service_tickets_bp.route("/", methods=["GET"])
def get_service_tickets():
    query = select(Service_Ticket)
    tickets = db.session.execute(query).scalars().all()
    
    return service_tickets_schema.jsonify(tickets), 200



# Many-to-Many relationship: Service ticket & Mechanic

# = 3. Assign a mechanic to a service ticket (PUT): 
@service_tickets_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=["PUT"])
def assign_mechanic(ticket_id, mechanic_id):
    
    # Check if ticket exists:
    ticket = db.session.get(Service_Ticket, ticket_id)
    if not ticket: 
        return jsonify({"error": "Service ticket not found."}), 404
    
    # Check if mechanic exists:
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    # Check if the mechanic is already assigned to this service ticket:
    if mechanic in ticket.mechanics:
        return jsonify({"message":"Mechanic is already assigned to this service ticket."}), 200
    
    # Assign the mechanic to the service ticket:
    ticket.mechanics.append(mechanic) # mechanics list
    db.session.commit()
        
    return service_ticket_schema.jsonify(ticket), 200
    
    

# = 4. Remove mechanic from service ticket (PUT): 
@service_tickets_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=["PUT"])
def remove_mechanic(ticket_id, mechanic_id):
    
    # Check if ticket exists:
    ticket = db.session.get(Service_Ticket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    
    # Check if mechanic exists:
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    # Check if the mechanic is not already assigned to this service ticket:
    if mechanic not in ticket.mechanics:
        return jsonify({"message":f"Mechanic is not assigned to this service ticket."}), 200
    
    # Remove the mechanic from the service ticket:
    ticket.mechanics.remove(mechanic) # mechanics list
    db.session.commit()
        
    return service_ticket_schema.jsonify(ticket), 200
