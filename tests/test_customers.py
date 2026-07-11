import unittest

from app import create_app
from app.models import db, Customer
from app.utils.util import encode_token

# Customer Route Tests:
class CustomerRouteTests(unittest.TestCase):  
    def setUp(self):
        # Create flask app using isolated testing config:
        self.app = create_app("TestingConfig") # test app instance.
        self.client = self.app.test_client()
        
        # Push app context so database operations can run:
        with self.app.app_context():
            # Resets test database before each test runs:
            db.drop_all() 
            db.create_all()
            
            # Create test customer:
            self.customer = Customer(
                name="test_user", 
                email="test@email.com", 
                phone="222-333-4444", 
                password="password123"
            )
            
            db.session.add(self.customer)
            db.session.commit()
        
            # Resuable values:
            self.customer_id = self.customer.id        
            self.token = encode_token(self.customer_id)
            
    # Remove active sessions & delete test tables after each test:
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            
            # Close all database connections held by SQLAlchemy:
            db.engine.dispose()
        
        
    # = Tests:
    # Create customer:
    def test_create_customer(self):
        customer_payload = {
            "name": "Test Customer",
            "email": "customer@test.com",
            "phone": "222-333-4444",
            "password": "password123"
        }
        
        response = self.client.post("/customers/", json=customer_payload)
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data["name"], "Test Customer")
        
    
    # Get all customers:
    def test_get_all_customers(self):
        response = self.client.get("/customers/?page=1&per_page=5") # pagination
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["total_customers"], 1)
        self.assertEqual(len(response_data["customers"]), 1)
  
    
    # Get single customer:
    def test_get_single_customer(self):
        response = self.client.get(f"/customers/{self.customer_id}")
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["id"], self.customer_id)
        self.assertEqual(response_data["email"], "test@email.com")
        
    # Customer login:
    def test_customer_login(self):
        credentials = {
            "email": "test@email.com",
            "password": "password123"
        } 
        
        response = self.client.post("/customers/login", json=credentials)
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["status"], "success")
        self.assertIn("token", response_data) # Returns JWT token.
        
    
    # Update customer:
    def test_update_customer(self):
        update_payload = {
            "name": "Updated Customer",
            "email": "updated@test.com",
            "phone": "222-333-4444",
            "password": "updatedpassword"
        }
        
        headers = {
            "Authorization": f"Bearer {self.token}"
            } # JWT token for protected route. 
        
        response = self.client.put("/customers/", json=update_payload, headers=headers)
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["name"], "Updated Customer")
        self.assertEqual(response_data["email"], "updated@test.com")
        
        
    # Delete customer:
    def test_delete_customer(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        
        response = self.client.delete("/customers/", headers=headers)
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["message"], "test_user has been successfully deleted.")

        # Query database directly to verify record was removed:
        with self.app.app_context():
            deleted_customer = db.session.get(Customer, self.customer_id)
            
            self.assertIsNone(deleted_customer) # Return none when customer no longer exists.
            
        
    # Get authenticated customer tickets:
    def test_get_my_tickets(self):
        headers = {
            "Authorization": f"Brearer {self.token}"
        }
        
        response = self.client.get("/customers/my-tickets", headers=headers)
        response_data = response.get_json()
        
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data, list)
        self.assertEqual(response_data, []) # returns empty list (setUp customer has no tickets).
    
if __name__ == "__main__":
    unittest.main()