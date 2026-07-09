from app.extensions import ma
from app.models import Customer

# = Customer schema:
class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        
# Initialize schema instances:
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

login_schema = CustomerSchema(exclude=["name", "phone"]) # token authentication login schema. 