import unittest

from app import create_app
from app.models import db, Customer
from app.utils.util import encode_token

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
        
            # Reusable values:
            self.customer_id = self.customer.id        
            self.token = encode_token(self.customer_id)
            
    # Remove active sessions & delete test tables after each test:
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            
            # Close all database connections held by SQLAlchemy:
            db.engine.dispose()
        
        
    # = Create customer:
    
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
        
    
    # * Negative test:
    
    def test_create_customer_duplicate_email(self):
        """Test creating a customer with an existing email."""
        
        duplicate_customer ={
            "name": "Jane Doe",
            "email": self.customer.email,
            "phone": "222-333-4444",
            "password": "password123"
        }
        
        response = self.client.post("/customers/", json=duplicate_customer)
        
        self.assertEqual(response.status_code, 400)
        
        response_data = response.get_json()
        
        self.assertIn("message", response_data)
        self.assertEqual(
            response_data["message"],
            "Email is already associated with an account."
            )
        
    
    # = Get all customers:
    
    def test_get_all_customers(self):
        response = self.client.get("/customers/?page=1&per_page=5")
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["total_customers"], 1)
        self.assertEqual(len(response_data["customers"]), 1)
  
    
    # = Get single customer:
    
    def test_get_single_customer(self):
        response = self.client.get(f"/customers/{self.customer_id}")
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["id"], self.customer_id)
        self.assertEqual(response_data["email"], "test@email.com")


    # * Negative test:
    
    def test_get_customer_not_found(self):
        """Test retrieving a customer that does not exist."""

        response = self.client.get("/customers/9999")
        self.assertEqual(response.status_code, 404)
        response_data = response.get_json()
        self.assertIn("error", response_data)
                   
    # = Customer login:
    
    def test_customer_login(self):
        credentials = {
            "email": "test@email.com",
            "password": "password123"
        } 
        
        response = self.client.post("/customers/login", json=credentials)
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["status"], "success")
        self.assertIn("token", response_data)
        
    # * Negative test:
     
    def test_customer_login_invalid_credentials(self):
        """Test customer login with an incorrect password."""

        credentials = {
            "email": self.customer.email,
            "password": "wrongpassword"
        }

        response = self.client.post("/customers/login", json=credentials)
        self.assertEqual(response.status_code, 401)
        response_data = response.get_json()
        
        self.assertIn("message", response_data)
        self.assertEqual(
            response_data["message"],
            "Invalid email or password! Please try again."
        )
     
    # = Update customer:
    
    def test_update_customer(self):
        update_payload = {
            "name": "Updated Customer",
            "email": "updated@test.com",
            "phone": "222-333-4444",
            "password": "updatedpassword"
        }
        
        headers = {
            "Authorization": f"Bearer {self.token}"
            }
        
        response = self.client.put("/customers/", json=update_payload, headers=headers)
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["name"], "Updated Customer")
        self.assertEqual(response_data["email"], "updated@test.com")
          
    # * Negative test:
     
    def test_update_customer_missing_token(self):
        """Test updating a customer without a JWT token."""

        updated_customer = {
            "name": "Updated Name",
            "email": "updated@email.com",
            "phone": "333-444-555",
            "password": "newpassword123"
        }

        response = self.client.put(
            "/customers/",
            json=updated_customer
        )

        self.assertEqual(response.status_code, 401)
        response_data = response.get_json()
        self.assertIn("message", response_data)        
               
    # = Delete customer:
    
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
            
            self.assertIsNone(deleted_customer)
               
    # * Negative test
     
    def test_delete_customer_missing_token(self):
        """Test deleting a customer without a JWT token."""

        response = self.client.delete("/customers/")

        self.assertEqual(response.status_code, 401)
        response_data = response.get_json()
        self.assertIn("message", response_data)
              
    # = Get authenticated customer tickets:
    
    def test_get_my_tickets(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        
        response = self.client.get("/customers/my-tickets", headers=headers)
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data, list)
        self.assertEqual(response_data, [])
           
    # * Negative test:
      
    def test_get_my_tickets_missing_token(self):
        """Test retrieving customer tickets without a JWT token."""

        response = self.client.get("/customers/my-tickets")
        
        self.assertEqual(response.status_code, 401)
        response_data = response.get_json()
        self.assertIn("message", response_data) 
 
      
if __name__ == "__main__":
    unittest.main()