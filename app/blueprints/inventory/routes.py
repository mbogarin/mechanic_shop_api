from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select

from . import inventory_bp
from app.models import db, Inventory
from .schemas import inventory_schema, inventories_schema

# INVENTORY ENDPOINTS:
# = 1. (POST) CREATE INVENTORY PART:
@inventory_bp.route("/", methods =["POST"])
def create_inventory_part():
    try:
        part_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_part = Inventory(
        name=part_data['name'],
        price=part_data['price']
    )
    
    db.session.add(new_part)
    db.session.commit()
    
    return inventory_schema.jsonify(new_part), 201


# = 2. (GET) RETRIEVE ALL INVENTORY PARTS:
@inventory_bp.route("/", methods =["GET"])
def get_inventory_parts():
    query = select(Inventory)
    parts = db.session.execute(query).scalars().all()
    
    return inventories_schema.jsonify(parts), 200
    

# = 3. (GET) RETRIEVE SINGLE INVENTORY PART BY ID:
@inventory_bp.route("/<int:part_id>", methods =["GET"])
def get_inventory_part(part_id):
    part = db.session.get(Inventory, part_id)
    
    if not part: 
        return jsonify({"message": "Inventory part not found."}), 404
    

    return inventory_schema.jsonify(part), 200



# = 4. (PUT) UPDATE INVENTORY PART BY ID:
@inventory_bp.route("/<int:part_id>", methods =["PUT"])
def update_inventory_part(part_id):
    part = db.session.get(Inventory, part_id)
    
    if not part: 
        return jsonify({"message": "Inventory part not found."}), 404
    
    try:
        part_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    part.name = part_data.get("name", part.name)
    part.price = part_data.get("price", part.price)
    
    db.session.commit()
    
    return inventory_schema.jsonify(part), 200
    

# = 5. (DELETE) DELETE INVENTORY PART BY ID:
@inventory_bp.route("/<int:part_id>", methods =["DELETE"])
def delete_inventory_part(part_id):
    part = db.session.get(Inventory, part_id)
    
    if not part: 
        return jsonify({"message": "Inventory part not found."}), 404
    
    db.session.delete(part)
    db.session.commit()

    return jsonify({"message": f"{part.name} was successfully deleted from inventory."}), 200

