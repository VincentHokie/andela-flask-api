
from flask import json
from app.views import app
from app.models import db

from app.tests.common_requests import CommonRequests

class LoginTestCase(CommonRequests):
    """This class represents the login test case"""

    def test_login(self):
        """Test API can create a user (POST request)"""

        with app.test_client() as client:
            self.sign_up(client, self.sign_up_credentials)

            login_credentials = {'username': 'vince', "password": "123"}
            res = self.login(client, login_credentials)

            self.assertEqual(res.status_code, 200)
            self.assertIn("success", json.loads(res.data))

    def test_login_password_required(self):
        """Test API can notice password is required (POST request)."""

        with app.test_client() as client:
            self.sign_up(client, self.sign_up_credentials)

            login_credentials = {'username': 'vince', "password": ""}
            res = self.login(client, login_credentials)

            self.assertEqual(res.status_code, 200)
            self.assertIn("error", json.loads(res.data))

    def test_login_username_required(self):
        """Test API can notice username is required (POST request)."""

        with app.test_client() as client:
            self.sign_up(client, self.sign_up_credentials)

            login_credentials = {'username': '', "password": "123"}
            res = self.login(client, login_credentials)

            self.assertEqual(res.status_code, 200)
            self.assertIn("error", json.loads(res.data))

    def tearDown(self):
        return False