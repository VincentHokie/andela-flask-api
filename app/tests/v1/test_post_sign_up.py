
from flask import json
from app import app

from app.tests.v1.common_requests import CommonRequests


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
            self.assertEqual(res.status_code, 422)

    def test_duplicate_email(self):
        """Test API can create a user (POST request)"""

        sign_up_credentials = {
            'username': 'vincex', "email": "andelatestmail@gmail.com",
            "password": "123", "password2": "123"}

        with app.test_client() as client:
            res = self.sign_up(client, sign_up_credentials)
            resp = json.loads(res.data)

            self.assertIn("error", resp)
            self.assertEqual(res.status_code, 422)
