from marshmallow import fields # to show assigned mechanics.
from app.extensions import ma
from app.models import Service_Ticket
from app.blueprints.mechanics.schemas import MechanicSchema


# = Service ticket schema:
class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested("MechanicSchema", many=True) # show assigned mechanics.
    customer = fields.Nested("CustomerSchema")
    class Meta:
        model = Service_Ticket
        include_fk = True # foreign key
        fields = ("id", "service_date", "service_desc", "customer_id", "customer", "mechanics")
        
        
# = Edit ticket schema:
class EditTicketSchema(ma.Schema):
    add_ids = fields.List(fields.Int(), load_default=[])
    remove_ids = fields.List(fields.Int(), load_default=[])
    class Meta:
        fields = ("add_ids", "remove_ids")
    
        
service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
return_ticket_schema = ServiceTicketSchema(exclude=["customer_id"])
edit_ticket_schema = EditTicketSchema()