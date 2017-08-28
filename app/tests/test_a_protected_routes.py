
import unittest
from app.views import app

from app.tests.common_requests import CommonRequests

class ProtectedRoutesTestCase(CommonRequests):
    """This class represents the sign up test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.define_db_connections(self.app)
        self.client = self.app.test_client
        self.credentials = {"username":"", "password":""}

    def test_create_shopping_list(self):
        """Test API wont submit if user is not authorized (POST request)"""

        with app.test_client() as client:
            res = self.create_shopping_list(client, {}, self.credentials)
            self.assertEqual(res.status_code, 401)

    def test_retrieve_shopping_list(self):
        """Test API wont submit if user is not authorized (GET request)"""

        with app.test_client() as client:
            res = self.get_all_shopping_list(self, client, self.credentials)
            self.assertEqual(res.status_code, 401)

    def test_retrieve_shopping_list_items(self):
        """Test API wont retirve resources if user is not authorized (GET request)"""

        with app.test_client() as client:
            res = self.get_items_under_shopping_list(self, client, 1, self.credentials)
            self.assertEqual(res.status_code, 401)

    def test_update_shopping_list(self):
        """Test API wont submit if user is not authorized (PUT request)"""

        with app.test_client() as client:
            res = self.update_shopping_list(client,  {}, 1, self.credentials)
            self.assertEqual(res.status_code, 401)

    def test_delete_shopping_list(self):
        """Test API wont submit if user is not authorized (DELETE request)"""

        with app.test_client() as client:
            res = self.delete_shopping_list(client, 1, self.credentials)
            self.assertEqual(res.status_code, 401)




    def test_create_shopping_list_item(self):
        """Test API wont submit if user is not authorized (POST request)"""

        with app.test_client() as client:
            res = self.create_shopping_list_item(client, {}, 1, self.credentials)
            self.assertEqual(res.status_code, 401)

    def test_update_shopping_list_item(self):
        """Test API wont submit if user is not authorized (PUT request)"""

        with app.test_client() as client:
            res = self.update_shopping_list_item(client, {}, 1, 1, self.credentials)
            self.assertEqual(res.status_code, 401)

    def test_delete_shopping_list_item(self):
        """Test API wont submit if user is not authorized (DELETE request)"""

        with app.test_client() as client:
            res = self.delete_shopping_list_item(client, 1, 1, self.credentials)
            self.assertEqual(res.status_code, 401)
