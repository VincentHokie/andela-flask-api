
from flask import json

import pytest
from app import app
from app.tests.v1.common_requests import CommonRequests


class ShoppingListTestCase(CommonRequests):
    """This class represents the shopping list test case"""

    def setUp(self):
        self.set_up_tests()
        CommonRequests.set_up_user_account(self)
        CommonRequests.set_up_authorized_route(self)

    def test_shopping_list_creation(self):
        """Test API can create a shopping list (POST request)"""

        with app.test_client() as client:

            shopping_list = {'name': 'vince'}
            res = self.create_shopping_list(client, shopping_list)
            back_data = json.loads(res.data)

            self.assertEqual(res.status_code, 201)
            self.assertEqual(back_data['name'], shopping_list["name"])
            CommonRequests.list_id = back_data["list_id"]

    def test_shopping_list_name_required(self):
        """Test API can create a shopping list (POST request)"""

        with app.test_client() as client:

            shopping_list = {'name': ''}
            res = self.create_shopping_list(client, shopping_list)
            back_data = json.loads(res.data)

            self.assertEqual(res.status_code, 422)
            self.assertIn("error", back_data)

    def test_api_can_get_all_shopping_lists(self):
        """Test API can get shopping lists (GET request)."""

        with app.test_client() as client:
            self.create_shopping_list(client, {'name': 'vince'})
            self.create_shopping_list(client, {'name': 'vince1'})
            self.create_shopping_list(client, {'name': 'vince2'})
            self.create_shopping_list(client, {'name': 'vince3'})
            self.create_shopping_list(client, {'name': 'vince4'})

            res = self.get_all_shopping_list(client)
            the_lists = json.loads(res.data)

            self.assertEqual(len(the_lists["lists"]), 5)
            self.assertEqual(res.status_code, 200)

    def test_api_cant_wont_allow_duplicate_shopping_lists(self):
        """Test API can get shopping lists (GET request)."""

        with app.test_client() as client:
            self.create_shopping_list(client, {'name': 'vince'})
            res = self.create_shopping_list(client, {'name': 'vince'})

            self.assertIn("error", json.loads(res.data))
            self.assertEqual(res.status_code, 406)

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

    def test_api_cant_wont_allow_duplicate_shopping_lists_on_update(self):
        """Test API can get shopping lists (GET request)."""

        with app.test_client() as client:
            self.create_shopping_list(client, {'name': 'vince1'})

            shopping_list = {'name': 'vince'}
            shopping_list_updated = {'name': 'vince1'}
            res = self.create_shopping_list(client, shopping_list)
            the_list = json.loads(res.data)

            res = self.update_shopping_list(
                client, shopping_list_updated, the_list['list_id'])

            self.assertIn("error", json.loads(res.data))
            self.assertEqual(res.status_code, 406)

    def test_api_invalid_form_update_shopping_list(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:

            shopping_list = {'name': 'vince'}
            shopping_list_updated = {'name': ''}
            res = self.create_shopping_list(client, shopping_list)
            the_list = json.loads(res.data)

            res = self.update_shopping_list(
                client, shopping_list_updated, the_list['list_id'])
            the_list = json.loads(res.data)

            self.assertEqual(res.status_code, 422)
            self.assertIn("error", the_list)

    def test_api_can_recognize_invalid_url_parameters_on_update(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:
            res = self.update_shopping_list(client, {}, "1a")
            the_list = json.loads(res.data)

            self.assertEqual(res.status_code, 422)
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

            self.assertEqual(result.status_code, 422)
            self.assertIn("error", json.loads(result.data))

    @pytest.mark.last
    def test_api_can_recognize_non_existent_url_parameters_on_delete(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:
            result = self.delete_shopping_list(client, "1111")

            self.assertEqual(result.status_code, 404)
            self.assertIn("error", json.loads(result.data))
