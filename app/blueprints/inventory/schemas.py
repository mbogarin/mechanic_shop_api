from app.extensions import ma
from app.models import Inventory


# Inventory schema:
class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        include_fk = True
        
        
# Initalize schemas:
inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)