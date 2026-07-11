from app import create_app
from app.models import db, Customer
from app.utils.util import encode_token
import unittest

class TestCustomer(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app("TestingConfig") # test app instance.
        self.customer = Customer(name="test_user", email="test@email.com", phone="123-456-7890", password="test-password")
        
        
        with self.app.app_context():
            db.drop_all() 
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
        self.token = encode_token(1)
        self.client = self.app.test_client()
        
    # Tests:
    
    # Create customer:
    def test_create_customer(self):
        customer_payload = {
            "name": "John Doe",
            "email": "jd@testemail.com",
            "phone": "123-456-7890",
            "password": "password123"
        }
        
        response = self.client.post("/customers/", json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["name"], "John Doe")
        
        
    # Customer login:
    def test_customer_login(self):
        credentials = {
            "email": "test@email.com",
            "password": "test-password"
        }
        
        response = self.client.post("/customers/login", json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "success")
        return response.get_json()["token"]
        
    
    # Update customer:
    def test_update_customer(self):
        update_payload = {
            "name": "Updated Customer",
            "email": "updated@test.com",
            "phone": "123-456-7890",
            "password": "updatedpassword"
        }
        
        headers = {"Authorization": "Bearer " + self.test_customer_login()}
        
        response = self.client.put("/customers/", json=update_payload, headers=headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Updated Customer")
        self.assertEqual(response.get_json()["email"], "updated@test.com")
        