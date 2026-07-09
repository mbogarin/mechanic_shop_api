from app.extensions import ma
from app.models import Customer
from marshmallow import fields

# = Customer schema:
class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        

# Pagination Customer Schema:
class PaginatedCustomerSchema(ma.Schema):
    customers = fields.Method("get_customers")
    total_customers = fields.Int(attribute="total")
    page = fields.Int()
    per_page = fields.Int()
    total_page = fields.Int(attribute="pages")
    has_next = fields.Bool()
    has_prev = fields.Bool()
    
    def get_customers(self, obj):
        return CustomerSchema(many=True).dump(obj.items)
    
        
        
        
# Initialize schema instances:
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_schema = CustomerSchema(exclude=["name", "phone"]) # token authentication login schema. 
paginated_customers_schema = PaginatedCustomerSchema() 