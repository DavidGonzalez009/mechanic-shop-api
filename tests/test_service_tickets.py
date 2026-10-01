import unittest

from application import create_app
from application.extensions import db
from application.models import Customer, Mechanic, ServiceTicket, Inventory
from application.utils.util import encode_token
from config import TestingConfig


class TestServiceTickets(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            customer = Customer(
                name="Test Customer",
                email="customer@example.com",
                phone="3125551234",
                password="test123"
            )

            mechanic = Mechanic(
                name="Test Mechanic",
                email="mechanic@example.com",
                phone="3125555678",
                salary=65000
            )

            inventory = Inventory(
                name="Test Oil Filter",
                price=19.99
            )

            db.session.add_all([
                customer,
                mechanic,
                inventory
            ])
            db.session.commit()

            self.customer_id = customer.id
            self.mechanic_id = mechanic.id
            self.inventory_id = inventory.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_service_ticket(self):
        ticket_payload = {
            "VIN": "1HGCM82633A123456",
            "service_date": "2026-10-01",
            "service_desc": "Oil change",
            "customer_id": self.customer_id
        }

        response = self.client.post(
            "/service-tickets/",
            json=ticket_payload
        )

        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["VIN"], "1HGCM82633A123456")
        self.assertEqual(data["service_desc"], "Oil change")


    def test_get_service_tickets(self):
        self.client.post("/service-tickets/", json={
            "VIN": "1HGCM82633A123456",
            "service_date": "2026-10-01",
            "service_desc": "Oil change",
            "customer_id": self.customer_id
        })

        response = self.client.get("/service-tickets/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)


    def test_get_my_tickets(self):
        self.client.post("/service-tickets/", json={
            "VIN": "1HGCM82633A123456",
            "service_date": "2026-10-01",
            "service_desc": "Oil change",
            "customer_id": self.customer_id
        })

        token = encode_token(self.customer_id)

        response = self.client.get(
            "/service-tickets/my-tickets",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)


    def test_assign_mechanic(self):
        self.client.post("/service-tickets/", json={
            "VIN": "1HGCM82633A123456",
            "service_date": "2026-10-01",
            "service_desc": "Oil change",
            "customer_id": self.customer_id
        })

        response = self.client.put(
            f"/service-tickets/1HGCM82633A123456/"
            f"assign-mechanic/{self.mechanic_id}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["message"],
            "Mechanic assigned successfully"
        )


    def test_remove_mechanic(self):
        self.client.post("/service-tickets/", json={
            "VIN": "1HGCM82633A123456",
            "service_date": "2026-10-01",
            "service_desc": "Oil change",
            "customer_id": self.customer_id
        })

        self.client.put(
            f"/service-tickets/1HGCM82633A123456/"
            f"assign-mechanic/{self.mechanic_id}"
        )

        response = self.client.put(
            f"/service-tickets/1HGCM82633A123456/"
            f"remove-mechanic/{self.mechanic_id}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["message"],
            "Mechanic removed successfully"
        )


    def test_edit_service_ticket_mechanics(self):
        self.client.post("/service-tickets/", json={
            "VIN": "1HGCM82633A123456",
            "service_date": "2026-10-01",
            "service_desc": "Oil change",
            "customer_id": self.customer_id
        })

        response = self.client.put(
            "/service-tickets/1HGCM82633A123456/edit",
            json={
                "add_ids": [self.mechanic_id],
                "remove_ids": []
            }
        )

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["mechanics"]), 1)


    def test_add_inventory_to_service_ticket(self):
        self.client.post("/service-tickets/", json={
            "VIN": "1HGCM82633A123456",
            "service_date": "2026-10-01",
            "service_desc": "Oil change",
            "customer_id": self.customer_id
        })

        response = self.client.put(
            f"/service-tickets/1HGCM82633A123456/"
            f"add-inventory/{self.inventory_id}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["message"],
            "Inventory item added successfully"
        )
        
if __name__ == "__main__":
    unittest.main()