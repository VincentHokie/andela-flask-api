
from flask import json

from app.views import app
from app.models import db, ShoppingList
from datetime import datetime
from app.tests.common_requests import CommonRequests


class ShoppingListTestCase(CommonRequests):
    """This class represents the shopping list test case"""

    def setUp(self):
        self.set_up_tests()
        self.set_up_authorized_route()


    def test_shopping_list_creation(self):
        """Test API can create a shopping list (POST request)"""

        with app.test_client() as client:

            shopping_list = {'name': 'vince'}
            res = self.create_shopping_list(client, shopping_list)
            back_data = json.loads(res.data)

            self.assertEqual(res.status_code, 201)
            self.assertEqual(back_data['name'], shopping_list["name"])
            self.list_id = back_data["list_id"]

    def test_shopping_list_name_required(self):
        """Test API can create a shopping list (POST request)"""

        with app.test_client() as client:

            shopping_list = {'name': ''}
            res = self.create_shopping_list(client, shopping_list)
            back_data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertIn("error", back_data)

    def test_api_can_get_all_shopping_lists(self):
        """Test API can get shopping lists (GET request)."""

        with app.test_client() as client:
            res = self.get_all_shopping_list(client)
            self.assertEqual(res.status_code, 200)

    # def test_api_can_get_single_shopping_list(self):
    #     """Test API can get shopping lists (GET request)."""
    #
    #     with app.test_client() as client:
    #         res = self.get_all_shopping_list(client, str(self.list_id))
    #         the_list = json.loads(res.data)
    #         self.assertEqual(res.status_code, 200)
    #         print( the_list )
    #         self.assertEqual(the_list.list_id, self.list_id)

    def test_api_can_update_shopping_list(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:

            shopping_list = {'name': 'vince'}
            shopping_list_updated = {'name': 'vince123'}
            res = self.create_shopping_list(client, shopping_list)
            the_list = json.loads(res.data)

            res = self.update_shopping_list(
                client, shopping_list_updated, the_list['list_id'])
            the_list = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertIn("success", the_list)

    def test_api_can_recognize_invalid_url_parameters_on_update(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:
            res = self.update_shopping_list(client, {}, "1a")
            the_list = json.loads(res.data)

            self.assertEqual(res.status_code, 500)
            self.assertIn("error", the_list)

    def test_api_can_recognize_non_existent_url_parameters_on_update(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:
            res = self.update_shopping_list(client, {}, "1111")
            the_list = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertIn("error", the_list)

    def test_api_can_delete_shopping_list(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:

            shopping_list = {'name': 'vince'}
            res = self.create_shopping_list(client, shopping_list)
            the_list = json.loads(res.data)

            result = self.delete_shopping_list(client, the_list['list_id'])

            self.assertEqual(result.status_code, 202)
            self.assertIn("success", json.loads(result.data))

    def test_api_can_recognize_invalid_url_parameters_on_delete(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:
            result = self.delete_shopping_list(client, "1a")

            self.assertEqual(result.status_code, 500)
            self.assertIn("error", json.loads(result.data))

    def test_api_can_recognize_non_existent_url_parameters_on_delete(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:
            result = self.delete_shopping_list(client, "1111")

            self.assertEqual(result.status_code, 404)
            self.assertIn("error", json.loads(result.data))


    def tearDown(self):
        return False