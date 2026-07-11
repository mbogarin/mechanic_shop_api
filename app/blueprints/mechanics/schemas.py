from app.extensions import ma
from app.models import Mechanic
from marshmallow import fields

# Mechanic schema:
class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        
# Mechanic Ticket Count schema:
class MechanicTicketCountSchema(MechanicSchema):
    ticket_count = fields.Method("get_ticket_count")
    
    def get_ticket_count(self, obj):
        return len(obj.service_tickets)
    
    
# Intitalize schema instances:
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
mechanic_ticket_count_schema = MechanicTicketCountSchema(many=True)

