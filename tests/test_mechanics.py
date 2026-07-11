import unittest

from app import create_app
from app.models import db, Mechanic, Customer


# Mechanic Route Tests:
class MechanicRouteTests(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.drop_all() 
            db.create_all()
        
            self.customer = Customer(
                name="Test Customer", 
                email="customer@test.com", 
                phone="222-333-4444", 
                password="password123"
            )
            
            self.mechanic = Mechanic(
                name="Test Mechanic", 
                email="mechanic@test.com", 
                phone="222-333-4444", 
                salary=65000.00
            )
            
            db.session.add_all([self.customer, self.mechanic])
            db.session.commit()
            
            # Resuable values:
            self.mechanic_id = self.mechanic.id
            
    # Remove active sessions & delete test tables after each test:
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            
            # Close all database connections held by SQLAlchemy:
            db.engine.dispose()

    # = TESTS:
    # Create mechanic:
    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "New Mechanic",
            "email": "newmechanic@test.com",
            "phone": "222-333-4444",
            "salary": 70000.00
        }
        
        response = self.client.post("/mechanics/", json=mechanic_payload)
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data["name"], "New Mechanic")
        self.assertEqual(response_data["email"], "newmechanic@test.com")
        self.assertEqual(response_data["salary"], 70000.00)
      
    # Get all mechanics:
    def test_get_all_mechanics(self):
        response = self.client.get("/mechanics/")
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data, list)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]["id"], self.mechanic_id)
        self.assertEqual(response_data[0]["email"], "mechanic@test.com")
        
    
    # Update mechanic:
    def test_update_mechanic(self):
        update_payload = {
            "name": "Updated Mechanic",
            "email": "updatedmechanic@test.com",
            "phone": "222-333-4444",
            "salary": 75000.00
        }
        
        response = self.client.put(f"/mechanics/{self.mechanic_id}", json=update_payload)
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["id"], self.mechanic_id)
        self.assertEqual(response_data["name"], "Updated Mechanic")
        self.assertEqual(response_data["email"], "updatedmechanic@test.com")
        self.assertEqual(response_data["salary"], 75000.00)
        
        # Verify updated values were committed:
        with self.app.app_context():
            updated_mechanic = db.session.get(
                Mechanic,
                self.mechanic_id
            )
            
            self.assertEqual(
                updated_mechanic.name,
                "Updated Mechanic"
            )
        
    
    # Delete mechanic:
    def test_delete_mechanic(self):
        response = self.client.delete(f"/mechanics/{self.mechanic_id}")
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_data["message"],
            "Test Mechanic was successfully deleted."
        )
        
        with self.app.app_context():
            deleted_mechanic = db.session.get(
                Mechanic,
                self.mechanic_id
            )
            self.assertIsNone(deleted_mechanic)
            
            
    # Rank mechanics by most tickets:
    def test_get_my_tickets(self):
        response = self.client.get("/mechanics/most-tickets")
        response_data = response.get_json()
        
        # No assigned tickets in setup (count = 0)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data, list)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(
            response_data[0]["id"],
            self.mechanic_id
        )
        self.assertEqual(response_data[0]["ticket_count"], 0)
    
    
if __name__ == "__main__":
    unittest.main()