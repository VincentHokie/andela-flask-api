
from flask import json
from app.views import app
from app.models import User

from app.tests.common_requests import CommonRequests

class PostSignUpTestCase(CommonRequests):
    """This class represents the sign up test case"""

    def setUp(self):
        self.set_up_tests()
        CommonRequests.set_up_user_account(self)

    def test_duplicate_username(self):
        """Test API can create a user (POST request)"""

        with app.test_client() as client:
            res = self.sign_up(client, CommonRequests.sign_up_credentials)
            resp = json.loads(res.data)

            self.assertIn("error", resp)
            self.assertEqual(res.status_code, 200)

    def test_duplicate_email(self):
        """Test API can create a user (POST request)"""

        sign_up_credentials = {
            'username': 'vincex', "email": "andelatestmail@gmail.com",
            "password": "123", "password2": "123"}

        with app.test_client() as client:
            res = self.sign_up(client, sign_up_credentials)
            resp = json.loads(res.data)

            self.assertIn("error", resp)
            self.assertEqual(res.status_code, 200)
