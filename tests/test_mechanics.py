import unittest

from application import create_app
from application.extensions import db
from config import TestingConfig


class TestMechanics(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "Test Mechanic",
            "email": "mechanic@example.com",
            "phone": "3125555678",
            "salary": 65000
        }

        response = self.client.post(
            "/mechanics/",
            json=mechanic_payload
        )

        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["name"], "Test Mechanic")
        self.assertEqual(data["email"], "mechanic@example.com")

    def test_get_mechanics(self):
        self.client.post("/mechanics/", json={
            "name": "Test Mechanic",
            "email": "mechanic@example.com",
            "phone": "3125555678",
            "salary": 65000
        })

        response = self.client.get("/mechanics/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_update_mechanic(self):
        create_response = self.client.post("/mechanics/", json={
            "name": "Test Mechanic",
            "email": "mechanic@example.com",
            "phone": "3125555678",
            "salary": 65000
        })

        mechanic_id = create_response.get_json()["id"]

        response = self.client.put(
            f"/mechanics/{mechanic_id}",
            json={"name": "Updated Mechanic"}
        )

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], "Updated Mechanic")

    def test_delete_mechanic(self):
        create_response = self.client.post("/mechanics/", json={
            "name": "Test Mechanic",
            "email": "mechanic@example.com",
            "phone": "3125555678",
            "salary": 65000
        })

        mechanic_id = create_response.get_json()["id"]

        response = self.client.delete(
            f"/mechanics/{mechanic_id}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["message"],
            "Mechanic deleted successfully"
        )

    def test_most_active_mechanics(self):
        self.client.post("/mechanics/", json={
            "name": "Test Mechanic",
            "email": "mechanic@example.com",
            "phone": "3125555678",
            "salary": 65000
        })

        response = self.client.get("/mechanics/most-active")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_update_mechanic_not_found(self):
        response = self.client.put(
            "/mechanics/999",
            json={"name": "Missing Mechanic"}
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.get_json()["message"],
            "Mechanic not found"
        )

    def test_delete_mechanic_not_found(self):
        response = self.client.delete("/mechanics/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.get_json()["message"],
            "Mechanic not found"
        )


if __name__ == "__main__":
    unittest.main()