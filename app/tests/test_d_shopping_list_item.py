
from flask import json

from app.views import app
from app.models import db, ShoppingListItem, ShoppingList
from datetime import datetime
from app.tests.common_requests import CommonRequests


class ShoppingListItemTestCase(CommonRequests):
    """This class represents the shopping list test case"""

    def setUp(self):
        self.set_up_tests()
        self.set_up_authorized_route()

    def test_shopping_list_item_creation(self):
        """Test API can create a shopping list (POST request)"""

        with app.test_client() as client:

            res = self.create_shopping_list(
                client, self.shopping_list)
            the_list = json.loads(res.data)

            shopping_list_item = {'name': 'List item', "amount": 1000}
            result = self.create_shopping_list_item(
                client, shopping_list_item, the_list['list_id'])

            self.assertEqual(result.status_code, 201)

    def test_shopping_list_name_required(self):
        """Test API can create a shopping list (POST request)"""

        with app.test_client() as client:

            res = self.create_shopping_list(
                client, self.shopping_list)
            the_list = json.loads(res.data)

            shopping_list_item = {'name': '', "amount": 1000}
            result = self.create_shopping_list_item(
                client, shopping_list_item, the_list['list_id'])

            self.assertEqual(result.status_code, 200)
            self.assertIn("error", json.loads(result.data))

    def test_shopping_list_amount_required(self):
        """Test API can create a shopping list (POST request)"""

        with app.test_client() as client:

            res = self.create_shopping_list(
                client, self.shopping_list)
            the_list = json.loads(res.data)

            shopping_list_item = {'name': 'List item', "amount": ""}
            result = self.create_shopping_list_item(
                client, shopping_list_item, the_list['list_id'])

            self.assertEqual(result.status_code, 200)
            self.assertIn("error", json.loads(result.data))

    def test_api_can_get_all_shopping_lists(self):
        """Test API can get shopping lists (GET request)."""

        with app.test_client() as client:

            res = self.create_shopping_list(
                client, self.shopping_list)
            the_list = json.loads(res.data)

            res = self.get_items_under_shopping_list(
                client, the_list['list_id'])
            self.assertEqual(res.status_code, 200)

    def test_api_can_update_shopping_list(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:

            res = self.create_shopping_list(
                client, self.shopping_list)
            the_list = json.loads(res.data)

            shopping_list_item = {'name': 'vince', "amount": 10000}
            shopping_list_item_updated = {'name': 'vince123', "amount": 2000}

            the_list_item = self.create_shopping_list_item(
                client, shopping_list_item, the_list['list_id'])
            the_list_item = json.loads(the_list_item.data)

            rv = self.update_shopping_list_item(
                client, shopping_list_item_updated, the_list['list_id'],
                the_list_item['item_id'])

            the_list = ShoppingListItem.query.filter_by(
                list_id=the_list['list_id']).first()
            the_list = the_list.serialize

            self.assertEqual(rv.status_code, 200)
            self.assertIn("success", json.loads(rv.data))
            self.assertEqual(
                the_list['name'], shopping_list_item_updated['name'])
            self.assertEqual(
                the_list['amount'], shopping_list_item_updated['amount'])

    def test_api_can_detect_invalid_item_id_on_update(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:

            rv = self.update_shopping_list_item(
                client, {}, "1", "1a")

            self.assertEqual(rv.status_code, 500)
            self.assertIn("error", json.loads(rv.data))

    def test_api_can_detect_invalid_list_id_on_update(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:

            rv = self.update_shopping_list_item(
                client, {}, "1a", "1")

            self.assertEqual(rv.status_code, 500)
            self.assertIn("error", json.loads(rv.data))

    def test_api_can_detect_non_existent_item_id_on_update(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:
            rv = self.update_shopping_list_item(
                client, {}, "1", "111")

            self.assertEqual(rv.status_code, 404)
            self.assertIn("error", json.loads(rv.data))

    def test_api_can_delete_shopping_list(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:

            res = self.create_shopping_list(
                client, self.shopping_list)
            the_list = json.loads(res.data)

            shopping_list_item = {'name': 'vince', "amount": 10000}
            the_list_item = self.create_shopping_list_item(
                client, shopping_list_item, the_list['list_id'])
            the_list_item = json.loads(the_list_item.data)

            the_list = ShoppingListItem.query.filter_by(
                list_id=the_list['list_id']).first()
            the_list = the_list.serialize

            result = self.delete_shopping_list_item(
                client, the_list['list_id'], the_list_item['item_id'])

            self.assertEqual(result.status_code, 202)
            self.assertEqual(None, ShoppingListItem.query.filter_by(
                item_id=the_list_item["item_id"]).first())

    def test_api_can_detect_non_existent_item_id_on_delete(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:
            rv = self.delete_shopping_list_item(
                client, "1", "111")

            self.assertEqual(rv.status_code, 404)
            self.assertIn("error", json.loads(rv.data))

    def test_api_can_detect_invalid_item_id_on_delete(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:
            rv = self.delete_shopping_list_item(
                client, "1", "1a")

            self.assertEqual(rv.status_code, 500)
            self.assertIn("error", json.loads(rv.data))

    def test_api_can_detect_invalid_list_id_on_delete(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:
            rv = self.delete_shopping_list_item(
                client, "1a", "1")

            self.assertEqual(rv.status_code, 500)
            self.assertIn("error", json.loads(rv.data))

    def tearDown(self):
        return False