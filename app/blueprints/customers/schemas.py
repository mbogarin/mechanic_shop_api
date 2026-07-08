from app.extensions import ma
from app.models import Customer

# = Customer schema:
class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        
# Initialize schema instances:
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)