from marshmallow import fields # to show assigned mechanics.
from app.extensions import ma
from app.models import Service_Ticket
from app.blueprints.customers.schemas import CustomerSchema
from app.blueprints.mechanics.schemas import MechanicSchema
from app.blueprints.inventory.schemas import InventorySchema


# Service Ticket schema:
class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    customer = fields.Nested(CustomerSchema)
    mechanics = fields.Nested(MechanicSchema, many=True)
    parts = fields.Nested(InventorySchema, many=True) 
    class Meta:
        model = Service_Ticket
        include_fk = True # foreign key
        fields = ("id", "VIN", "service_date", "service_desc", "customer_id", "customer", "mechanics", "parts")

 

# Edit Ticket schema: (custom schema)
class EditTicketSchema(ma.Schema):
    add_ids = fields.List(fields.Int(), load_default=[])
    remove_ids = fields.List(fields.Int(), load_default=[])
    class Meta:
        fields = ("add_ids", "remove_ids")
    

# Intialize Schemas:
service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
return_ticket_schema = ServiceTicketSchema(exclude=["customer_id"])
edit_ticket_schema = EditTicketSchema()