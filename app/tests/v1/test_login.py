
from flask import json
from app import app

from app.tests.v1.common_requests import CommonRequests


class LoginTestCase(CommonRequests):
    """This class represents the login test case"""

    def setUp(self):
        self.set_up_tests()
        CommonRequests.set_up_user_account(self)

    def test_login(self):
        """Test API can create a user (POST request)"""

        with app.test_client() as client:

            res = self.login(client, CommonRequests.login_credentials)

            self.assertEqual(res.status_code, 200)
            self.assertIn("success", json.loads(res.data))

    def test_wrong_credentials_login(self):
        """Test API can create a user (POST request)"""

        with app.test_client() as client:

            res = self.login(client, {
                'username': 'wrong', "password": "wrong"
                })

            self.assertEqual(res.status_code, 401)
            self.assertIn("error", json.loads(res.data))

    def test_login_password_required(self):
        """Test API can notice password is required (POST request)."""

        with app.test_client() as client:
            res = self.login(client, {'username': 'vince', "password": ""})

            self.assertEqual(res.status_code, 422)
            self.assertIn("error", json.loads(res.data))

    def test_login_username_required(self):
        """Test API can notice username is required (POST request)."""

        with app.test_client() as client:
            res = self.login(client, {'username': '', "password": "123"})

            self.assertEqual(res.status_code, 422)
            self.assertIn("error", json.loads(res.data))
