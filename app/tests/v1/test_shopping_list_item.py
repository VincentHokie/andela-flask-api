
from flask import json

from app import app
from app.models import ShoppingListItem
from app.tests.v1.common_requests import CommonRequests


class ShoppingListItemTestCase(CommonRequests):
    """This class represents the shopping list test case"""

    def setUp(self):
        self.set_up_tests()
        CommonRequests.set_up_user_account(self)
        CommonRequests.set_up_authorized_route(self)
        CommonRequests.set_up_shopping_list(self)

    def test_shopping_list_item_creation(self):
        """Test API can create a shopping list (POST request)"""

        with app.test_client() as client:

            shopping_list_item = {'name': 'List item', "amount": 1000}
            result = self.create_shopping_list_item(
                client, shopping_list_item, CommonRequests.list_id)

            self.assertEqual(result.status_code, 201)

    def test_shopping_list_item_name_required(self):
        """Test API can create a shopping list (POST request)"""

        with app.test_client() as client:

            shopping_list_item = {'name': '', "amount": 1000}
            result = self.create_shopping_list_item(
                client, shopping_list_item, CommonRequests.list_id)

            self.assertEqual(result.status_code, 200)
            self.assertIn("error", json.loads(result.data))

    def test_shopping_list_item_amount_required(self):
        """Test API can create a shopping list (POST request)"""

        with app.test_client() as client:

            shopping_list_item = {'name': 'List item', "amount": ""}
            result = self.create_shopping_list_item(
                client, shopping_list_item, CommonRequests.list_id)

            self.assertEqual(result.status_code, 200)
            self.assertIn("error", json.loads(result.data))

    def test_api_can_get_all_shopping_list_items(self):
        """Test API can get shopping lists (GET request)."""

        with app.test_client() as client:

            res = self.get_items_under_shopping_list(
                client, CommonRequests.list_id)
            self.assertEqual(res.status_code, 200)

    def test_api_can_update_shopping_list_item(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:

            shopping_list_item_updated = {'name': 'vince123', "amount": 2000}
            shopping_list_item = {'name': 'List item', "amount": 890}
            result = self.create_shopping_list_item(
                client, shopping_list_item, CommonRequests.list_id)
            shl_object = json.loads(result.data)

            rv = self.update_shopping_list_item(
                client, shopping_list_item_updated, CommonRequests.list_id,
                shl_object['item_id'])

            the_list = ShoppingListItem.query.filter_by(
                item_id=shl_object['item_id']).first()
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
                client, {}, CommonRequests.list_id, "1a")

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
                client, {}, CommonRequests.list_id, "111")

            self.assertEqual(rv.status_code, 404)
            self.assertIn("error", json.loads(rv.data))

    def test_api_can_delete_shopping_list_item(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:

            shopping_list_item = {'name': 'vince', "amount": 10000}
            the_list_item = self.create_shopping_list_item(
                client, shopping_list_item, CommonRequests.list_id)
            the_list_item = json.loads(the_list_item.data)

            the_list = ShoppingListItem.query.filter_by(
                list_id=CommonRequests.list_id).first()
            the_list = the_list.serialize

            result = self.delete_shopping_list_item(
                client, CommonRequests.list_id, the_list_item['item_id'])

            self.assertEqual(result.status_code, 202)
            self.assertEqual(None, ShoppingListItem.query.filter_by(
                item_id=the_list_item["item_id"]).first())

    def test_api_can_detect_non_existent_item_id_on_delete(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:
            rv = self.delete_shopping_list_item(
                client, CommonRequests.list_id, "111")

            self.assertEqual(rv.status_code, 404)
            self.assertIn("error", json.loads(rv.data))

    def test_api_can_detect_invalid_item_id_on_delete(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:
            rv = self.delete_shopping_list_item(
                client, CommonRequests.list_id, "1a")

            self.assertEqual(rv.status_code, 500)
            self.assertIn("error", json.loads(rv.data))

    def test_api_can_detect_invalid_list_id_on_delete(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:
            rv = self.delete_shopping_list_item(
                client, "1a", "1")

            self.assertEqual(rv.status_code, 500)
            self.assertIn("error", json.loads(rv.data))