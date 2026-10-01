import unittest

from application import create_app
from application.extensions import db
from config import TestingConfig


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_inventory_item(self):
        return self.client.post("/inventory/", json={
            "name": "Oil Filter",
            "price": 19.99
        })

    def test_create_inventory(self):
        response = self.create_inventory_item()

        self.assertEqual(response.status_code, 201)

        data = response.get_json()
        self.assertEqual(data["name"], "Oil Filter")
        self.assertEqual(data["price"], 19.99)

    def test_get_inventory(self):
        self.create_inventory_item()

        response = self.client.get("/inventory/")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Oil Filter")

    def test_get_inventory_item(self):
        create_response = self.create_inventory_item()
        inventory_id = create_response.get_json()["id"]

        response = self.client.get(f"/inventory/{inventory_id}")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data["name"], "Oil Filter")

    def test_update_inventory(self):
        create_response = self.create_inventory_item()
        inventory_id = create_response.get_json()["id"]

        response = self.client.put(
            f"/inventory/{inventory_id}",
            json={
                "name": "Premium Oil Filter",
                "price": 24.99
            }
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data["name"], "Premium Oil Filter")
        self.assertEqual(data["price"], 24.99)

    def test_delete_inventory(self):
        create_response = self.create_inventory_item()
        inventory_id = create_response.get_json()["id"]

        response = self.client.delete(f"/inventory/{inventory_id}")

        self.assertEqual(response.status_code, 200)

    # BONUS: negative tests

    def test_get_inventory_item_not_found(self):
        response = self.client.get("/inventory/999")

        self.assertEqual(response.status_code, 404)

    def test_update_inventory_not_found(self):
        response = self.client.put(
            "/inventory/999",
            json={
                "name": "Missing Part",
                "price": 10.00
            }
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_inventory_not_found(self):
        response = self.client.delete("/inventory/999")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()