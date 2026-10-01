import unittest

from application import create_app
from application.extensions import db
from config import TestingConfig


class TestCustomers(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_customer(self):
        customer_payload = {
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "3125551234",
            "password": "test123"
        }

        response = self.client.post(
            "/customers",
            json=customer_payload
        )

        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["name"], "Test Customer")
        self.assertEqual(data["email"], "test@example.com")

    def test_get_customers(self):
        self.client.post("/customers", json={
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "3125551234",
            "password": "test123"
        })

        response = self.client.get("/customers")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)


    def test_get_customer_by_id(self):
        create_response = self.client.post("/customers", json={
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "3125551234",
            "password": "test123"
        })

        customer_id = create_response.get_json()["id"]

        response = self.client.get(f"/customers/{customer_id}")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], "Test Customer")


    def test_update_customer(self):
        create_response = self.client.post("/customers", json={
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "3125551234",
            "password": "test123"
        })

        customer_id = create_response.get_json()["id"]

        response = self.client.put(
            f"/customers/{customer_id}",
            json={"name": "Updated Customer"}
        )

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], "Updated Customer")


    def test_delete_customer(self):
        create_response = self.client.post("/customers", json={
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "3125551234",
            "password": "test123"
        })

        customer_id = create_response.get_json()["id"]

        response = self.client.delete(f"/customers/{customer_id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["message"],
            "Customer deleted successfully"
        )


    def test_login_customer(self):
        self.client.post("/customers", json={
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "3125551234",
            "password": "test123"
        })

        response = self.client.post("/customers/login", json={
            "email": "test@example.com",
            "password": "test123"
        })

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], "success")
        self.assertIn("auth_token", data)


    def test_invalid_login(self):
        self.client.post("/customers", json={
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "3125551234",
            "password": "test123"
        })

        response = self.client.post("/customers/login", json={
            "email": "test@example.com",
            "password": "wrongpassword"
        })

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.get_json()["message"],
            "Invalid email or password"
        )


    def test_customer_not_found(self):
        response = self.client.get("/customers/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.get_json()["message"],
            "Customer not found"
        )
        
if __name__ == "__main__":
    unittest.main()