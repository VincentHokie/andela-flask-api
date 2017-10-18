
from flask import json

from app import app
from app.models import ShoppingListItem
from app.tests.v2.common_requests import CommonRequestsv2


class ShoppingListItemTestCase(CommonRequestsv2):
    """This class represents the shopping list test case"""

    def setUp(self):
        self.set_up_tests()
        CommonRequestsv2.set_up_user_account(self)
        CommonRequestsv2.set_up_authorized_route(self)
        CommonRequestsv2.set_up_shopping_list(self)
        CommonRequestsv2.set_up_shopping_list_item(self)

    def test_api_can_get_all_shopping_list_items_invalid_list_id(self):
        """Test API can get shopping lists (GET request)."""

        with app.test_client() as client:

            res = self.get_all_shopping_list_items(client, str("1a"))
            the_list = json.loads(res.data)

            self.assertEqual(res.status_code, 422)
            self.assertIn("error", the_list)

    def test_api_can_get_all_shopping_list_items_non_existent_list_id(self):
        """Test API can get shopping lists (GET request)."""

        with app.test_client() as client:

            res = self.get_all_shopping_list_items(client, str("1a"))
            the_list = json.loads(res.data)

            self.assertEqual(res.status_code, 422)
            self.assertIn("error", the_list)

    def test_api_can_get_all_shopping_list_items(self):
        """Test API can get shopping lists (GET request)."""

        with app.test_client() as client:
            
            CommonRequestsv2.set_up_shopping_list_item(self)
            CommonRequestsv2.set_up_shopping_list_item(self)
            CommonRequestsv2.set_up_shopping_list_item(self)
            CommonRequestsv2.set_up_shopping_list_item(self)

            res = self.get_all_shopping_list_items(client, CommonRequestsv2.list_id)
            the_list = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(the_list["count"], 5)
            self.assertIn("success", the_list)

    def test_api_can_get_all_shopping_list_items(self):
        """Test API can get shopping lists (GET request)."""

        with app.test_client() as client:
            
            self.create_shopping_list_item(
                client, {"name": "list1", "amount": 1}, 
                CommonRequestsv2.list_id)
            self.create_shopping_list_item(
                client, {"name": "list2", "amount": 1}, 
                CommonRequestsv2.list_id)
            self.create_shopping_list_item(
                client, {"name": "list11", "amount": 1}, 
                CommonRequestsv2.list_id)
            self.create_shopping_list_item(
                client, {"name": "list3", "amount": 1}, 
                CommonRequestsv2.list_id)

            res = self.get_all_shopping_list_items(client, CommonRequestsv2.list_id, "1")
            the_list = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(the_list["count"], 2)

    def test_api_can_get_single_shopping_list_item_invalid_list_id(self):
        """Test API can get shopping lists (GET request)."""

        with app.test_client() as client:

            res = self.get_single_shopping_list_item(client, str("1a"), 1)
            the_list = json.loads(res.data)

            self.assertEqual(res.status_code, 422)
            self.assertIn("error", the_list)

    def test_api_can_get_single_shopping_list_item_invalid_item_id(self):
        """Test API can get shopping lists (GET request)."""

        with app.test_client() as client:

            res = self.get_single_shopping_list_item(client, 1, "1a")
            the_list = json.loads(res.data)

            self.assertEqual(res.status_code, 422)
            self.assertIn("error", the_list)

    def test_api_can_get_single_shopping_list_non_existent(self):
        """Test API can get shopping lists (GET request)."""

        with app.test_client() as client:

            res = self.get_single_shopping_list_item(client, "111", 1)
            the_list = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertIn("error", the_list)

    def test_api_can_get_single_shopping_list_item_non_existent(self):
        """Test API can get shopping lists (GET request)."""

        with app.test_client() as client:

            res = self.get_single_shopping_list_item(client, 1, "111")
            the_list = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertIn("error", the_list)

    def test_api_can_get_single_shopping_list_item(self):
        """Test API can get shopping lists (GET request)."""

        with app.test_client() as client:

            res = self.get_single_shopping_list_item(
                client, CommonRequestsv2.list_id, CommonRequestsv2.item_id)
            the_list = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(the_list["item_id"], CommonRequestsv2.item_id)
