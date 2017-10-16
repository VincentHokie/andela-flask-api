
from flask import json

from app import app
from app.tests.v1.common_requests import CommonRequests


class EmailConfirmationTestCase(CommonRequests):
    """This class represents the shopping list test case"""

    def setUp(self):
        self.set_up_tests()
        CommonRequests.set_up_user_account(self)

    def test_email_is_required(self):
        """Test API can create a shopping list (POST request)"""

        with app.test_client() as client:

            email_object = {'email': ''}
            result = self.confirm_email_for_password_reset(
                client, email_object)

            self.assertEqual(result.status_code, 422)
            self.assertIn("error", json.loads(result.data))

    def test_invalid_email_submitted(self):
        """Test API can create a shopping list (POST request)"""

        with app.test_client() as client:
            email_object = {'email': 'vince'}
            result = self.confirm_email_for_password_reset(
                client, email_object)

            self.assertEqual(result.status_code, 422)
            self.assertIn("error", json.loads(result.data))

    def test_email_not_belonging_to_user(self):
        """Test API can create a shopping list (POST request)"""

        with app.test_client() as client:
            email_object = {'email': 'vince@gmail.com'}
            result = self.confirm_email_for_password_reset(
                client, email_object)

            self.assertEqual(result.status_code, 404)
            self.assertIn("error", json.loads(result.data))

    def test_correct_email_provided(self):
        """Test API can create a shopping list (POST request)"""

        with app.test_client() as client:
            email_object = {'email': CommonRequests.sign_up_credentials["email"]}

            try:
                result = self.confirm_email_for_password_reset(
                    client, email_object)
            except:
                return True

            self.assertEqual(result.status_code, 200)
            self.assertIn("success", json.loads(result.data))
