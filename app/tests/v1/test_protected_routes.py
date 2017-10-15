
from app import app

from app.tests.v1.common_requests import CommonRequests

class ProtectedRoutesTestCase(CommonRequests):
    """This class represents the sign up test case"""

    def test_create_shopping_list(self):
        """Test API wont submit if user is not authorized (POST request)"""

        with app.test_client() as client:
            res = self.create_shopping_list(client, {})
            self.assertEqual(res.status_code, 401)

    def test_retrieve_shopping_list(self):
        """Test API wont submit if user is not authorized (GET request)"""

        with app.test_client() as client:
            res = self.get_all_shopping_list(client)
            self.assertEqual(res.status_code, 401)

    def test_retrieve_shopping_list_items(self):
        """Test API wont retirve resources if user is not authorized (GET )"""

        with app.test_client() as client:
            res = self.get_items_under_shopping_list(
                client, 1)
            self.assertEqual(res.status_code, 401)

    def test_update_shopping_list(self):
        """Test API wont submit if user is not authorized (PUT request)"""

        with app.test_client() as client:
            res = self.update_shopping_list(client,  {}, 1)
            self.assertEqual(res.status_code, 401)

    def test_delete_shopping_list(self):
        """Test API wont submit if user is not authorized (DELETE request)"""

        with app.test_client() as client:
            res = self.delete_shopping_list(client, 1)
            self.assertEqual(res.status_code, 401)

    def test_create_shopping_list_item(self):
        """Test API wont submit if user is not authorized (POST request)"""

        with app.test_client() as client:
            res = self.create_shopping_list_item(
                client, {}, 1)
            self.assertEqual(res.status_code, 401)

    def test_update_shopping_list_item(self):
        """Test API wont submit if user is not authorized (PUT request)"""

        with app.test_client() as client:
            res = self.update_shopping_list_item(
                client, {}, 1, 1)
            self.assertEqual(res.status_code, 401)

    def test_delete_shopping_list_item(self):
        """Test API wont submit if user is not authorized (DELETE request)"""

        with app.test_client() as client:
            res = self.delete_shopping_list_item(client, 1, 1)
            self.assertEqual(res.status_code, 401)

    def test_logout(self):

        with app.test_client() as client:
            res = self.logout(client)
            self.assertEqual(res.status_code, 401)
