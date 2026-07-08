from marshmallow import fields

from app.extensions import ma
from app.models import Service_Ticket
from app.blueprints.mechanics.schemas import MechanicSchema



# Service_tickets schema:
class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested(MechanicSchema, many=True) # show assigned mechanics.
    class Meta:
        model = Service_Ticket
        include_fk = True # foreign key
        
        
service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)