import unittest

from app import create_app
from app.models import db, Inventory

# Inventory Route Tests:
class InventoryRouteTests(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            self.inventory_part = Inventory(
                name="Brake Pads",
                price=89.99
            )

            db.session.add(self.inventory_part)
            db.session.commit()
            
            self.part_id = self.inventory_part.id
            
    # Clean up database after every test:        
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()


    # TESTS:
    # = Create inventory part:
    def test_create_inventory_part(self):
        part_payload = {
            "name": "Oil Filter",
            "price": 24.99
        }
        
        response = self.client.post("/inventory/", json=part_payload)
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data["name"], "Oil Filter")
        self.assertEqual(response_data["price"], 24.99)
    
    
    # = Get all inventory parts:
    def test_get_all_parts(self):
        response = self.client.get("/inventory/")
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data, list)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]["id"], self.part_id)
        self.assertEqual(response_data[0]["name"], "Brake Pads")
        self.assertEqual(response_data[0]["price"], 89.99)
        
        
    # = Get single inventory part:
    def test_get_single_part(self):
        response = self.client.get(f"/inventory/{self.part_id}")
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["id"], self.part_id)
        self.assertEqual(response_data["name"], "Brake Pads")
        self.assertEqual(response_data["price"], 89.99)
    
    
     # * Negative test
    def test_get_inventory_part_not_found(self):
        """Test retrieving an inventory part that does not exist""" 
        
        response = self.client.get("/inventory/9999")
        
        self.assertEqual(response.status_code, 404)
        response_data = response.get_json()
        
        self.assertIn("message", response_data)
        self.assertEqual(
            response_data["message"],
            "Inventory part not found."
        )
        
        
        
    # = Update inventory part:
    def test_update_inventory_part(self):
        # Route supports partial updates - only change price:
        update_payload = {
            "price": 99.99
        }
        
        response = self.client.put(f"/inventory/{self.part_id}", json=update_payload)
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["id"], self.part_id)
        self.assertEqual(response_data["name"], "Brake Pads")
        self.assertEqual(response_data["price"], 99.99)
        
        # Verify updated values were committed:
        with self.app.app_context():
            updated_part = db.session.get(
                Inventory,
                self.part_id
            )
            
            self.assertIsNotNone(updated_part)
            assert updated_part is not None 
            
            self.assertEqual(
                updated_part.price,
                99.99
            )
    
    
    # = Delete inventory part:
    def test_delete_inventory_part(self):
        response = self.client.delete(f"/inventory/{self.part_id}")
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_data["message"],
            "Brake Pads was successfully deleted from inventory."
        )
        
        with self.app.app_context():
            deleted_part = db.session.get(
                Inventory,
                self.part_id
            )
            self.assertIsNone(deleted_part)
    
    
    
    
if __name__ == "__main__":
    unittest.main()