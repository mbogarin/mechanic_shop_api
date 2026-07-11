import unittest

from app import create_app
from app.models import db, Service_Ticket, Customer, Mechanic, Inventory

# Service Ticket Route Tests:
class ServiceTicketRouteTests(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            # Create customer required by service-ticket records:
            self.customer = Customer(
                name="Test Customer",
                email="customer@test.com",
                phone="222-333-4444",
                password="password123"
            )

            # Create mechanics for assignment/removal/edit tests:
            self.mechanic = Mechanic(
                name="Test Mechanic",
                email="mechanic@test.com",
                phone="222-333-4444",
                salary=65000.00
            )
            
            self.second_mechanic = Mechanic(
                name="Second Mechanic",
                email="secondmechanic@test.com",
                phone="222-333-4444",
                salary=70000.00
            )
            
            # Create an inventory part for the add-part route:
            self.inventory_part = Inventory(
                name="Brake Pads",
                price=89.99
            )
            
            db.session.add_all([
                self.customer,
                self.mechanic,
                self.second_mechanic,
                self.inventory_part
            ])
            db.session.commit()
            
            # Create an exisiting service ticket for routes:
            self.service_ticket = Service_Ticket(
                VIN="1HGCM82633A123456",
                service_date="07/11/2026",
                service_desc="Brake inspection",
                customer_id=self.customer.id
            )
            
            db.session.add(self.service_ticket)
            db.session.commit()
            
            
            # Store generated IDs before leaving app context:
            self.customer_id = self.customer.id
            self.mechanic_id = self.mechanic.id
            self.second_mechanic_id = self.second_mechanic.id
            self.part_id = self.inventory_part.id
            self.ticket_id = self.service_ticket.id
            
    # Clean up database after every test:        
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    # = TESTS:
    # = Create service ticket:
    def test_create_service_ticket(self):
        ticket_payload = {
            "VIN": "2C4RC1BG5KR654321",
            "service_date": "07/12/2026",
            "service_desc": "Oil change",
            "customer_id": self.customer_id
        }
        
        response = self.client.post("/service-tickets/", json=ticket_payload)
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data["VIN"], "2C4RC1BG5KR654321")
        self.assertEqual(response_data["service_desc"], "Oil change")
        self.assertEqual(response_data["customer_id"], self.customer_id)
    
    
    # = Get all service tickets:
    def test_get_all_service_tickets(self):
        response = self.client.get("/service-tickets/")
        response_data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data, list)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]["id"], self.ticket_id)
        self.assertEqual(response_data[0]["VIN"], "1HGCM82633A123456")
    
    
    # = Assign mechanic to service ticket:
    def test_assign_mechanic_to_service_ticket(self):
        response = self.client.put(f"/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}")
        response_data = response.get_json()
        
        # Confirm mechanic appears in ticket response:
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data['mechanics']), 1)
        self.assertEqual(response_data["mechanics"][0]["id"], self.mechanic_id)
        
        # Verify relationship was committed to database:
        with self.app.app_context():
            updated_ticket = db.session.get(
                Service_Ticket,
                self.ticket_id
            )
            
            self.assertIsNotNone(updated_ticket)
            assert updated_ticket is not None
            
            assigned_ids = [
                mechanic.id
                for mechanic in updated_ticket.mechanics
            ]
            
            self.assertIn(
                self.mechanic_id,
                assigned_ids
                )
    
    # = Remove mechanic from service ticket:
    def test_remove_mechanic_from_service_ticket(self):
        
        # Assign mechanic before testing its removal:
        with self.app.app_context():
            ticket = db.session.get(
                Service_Ticket,
                self.ticket_id
            )
            
            mechanic = db.session.get(
                Mechanic,
                self.mechanic_id
            )
            
            # Confirm both records before creating relationship:
            self.assertIsNotNone(ticket)
            self.assertIsNone(mechanic)
            
            assert ticket is not None
            assert mechanic is not None
            
            ticket.mechanics.append(mechanic)
            db.session.commit()
            
            # confirm mechanic was assigned before testing removal:
            self.assertIn(
                self.mechanic_id,
                [
                    assigned_mechanic.id
                    for assigned_mechanic in ticket.mechanics
                ]
            )
                        
        response = self.client.put(f"/service-tickets/{self.ticket_id}/remove-mechanic/{self.mechanic_id}")
        response_data = response.get_json()
        
        # Confirm response shows no assigned mechanics:
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['mechanics'], [])
        
        # Verify relationship was removed from database:
        with self.app.app_context():
            updated_ticket = db.session.get(
                Service_Ticket,
                self.ticket_id
            )
            
            # Confirm ticket still exists before checking relationship:
            self.assertIsNotNone(updated_ticket)
            assert updated_ticket is not None
            
            assigned_ids = [
                mechanic.id
                for mechanic in updated_ticket.mechanics
            ]
            
            self.assertNotIn(
                self.mechanic_id,
                assigned_ids
            )
    
    
    # = Edit service ticket mechanics:
    def test_edit_service_ticket_mechanics(self):
        # Assign 2nd mechanic so route can remove them:
        with self.app.app_context():
            ticket = db.session.get(
                Service_Ticket,
                self.ticket_id
                )
            
            second_mechanic = db.session.get(
                Mechanic,
                self.second_mechanic_id)
            
            self.assertIsNotNone(ticket)
            self.assertIsNone(second_mechanic)
            
            assert ticket is not None
            assert second_mechanic is not None
            
            ticket.mechanics.append(second_mechanic)
            db.session.commit()
            
        edit_payload = {
            "add_ids": [self.mechanic_id],
            "remove_ids": [self.second_mechanic_id]
        }
        
        response = self.client.put(f"/service-tickets/{self.ticket_id}/edit", json=edit_payload)
        response_data = response.get_json()
            
        # confirm 1st mechanic was added & 2nd was removed:
        self.assertEqual(response.status_code, 200)
        
        returned_mechanic_ids = [
            mechanic["id"] for mechanic in response_data["mechanics"]
        ]
        
        self.assertIn(self.mechanic_id, returned_mechanic_ids)
        self.assertNotIn(self.second_mechanic_id, returned_mechanic_ids)
    
    
    # = Add inventory part to service ticket:
    def test_add_inventory_part_to_service_ticket(self):
        response = self.client.put(f"/service-tickets/{self.ticket_id}/add-part/{self.part_id}")
        response_data = response.get_json()
        
        # Confirm inventory parts appear in ticket response:
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data["parts"]), 1)
        self.assertEqual(
            response_data["parts"][0]["id"],
            self.part_id
        )
        self.assertEqual(
            response_data["parts"][0]["name"],
            "Brake Pads"
        )
    
        with self.app.app_context():
            updated_ticket = db.session.get(
                Service_Ticket,
                self.ticket_id
            )
            
            self.assertIsNotNone(updated_ticket)
            assert updated_ticket is not None
            
            part_ids = [
                part.id
                for part in updated_ticket.parts
            ]
            
            self.assertIn(
                self.part_id,
                part_ids
            )
        
    
if __name__ == "__main__":
    unittest.main()