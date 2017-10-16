
from flask import json

from app import app
from app.tests.v2.common_requests import CommonRequestsv2


class ShoppingListTestCase(CommonRequestsv2):
    """This class represents the shopping list test case"""

    def setUp(self):
        self.set_up_tests()
        CommonRequestsv2.set_up_user_account(self)
        CommonRequestsv2.set_up_authorized_route(self)
        CommonRequestsv2.set_up_shopping_list(self)

    def test_api_can_get_single_shopping_list_invalid_id(self):
        """Test API can get shopping lists (GET request)."""

        with app.test_client() as client:

            res = self.get_single_shopping_list(client, str("1a"))
            the_list = json.loads(res.data)

            self.assertEqual(res.status_code, 422)
            self.assertIn("error", the_list)

    def test_api_can_get_single_shopping_list_non_existent(self):
        """Test API can get shopping lists (GET request)."""

        with app.test_client() as client:

            res = self.get_single_shopping_list(client, "111")
            the_list = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertIn("error", the_list)

    def test_api_can_get_single_shopping_list(self):
        """Test API can get shopping lists (GET request)."""

        with app.test_client() as client:

            res = self.get_single_shopping_list(
                client, CommonRequestsv2.list_id)
            the_list = json.loads(res.data)
            
            self.assertEqual(res.status_code, 200)
            self.assertEqual(the_list["list_id"], CommonRequestsv2.list_id)
