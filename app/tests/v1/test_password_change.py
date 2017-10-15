
from flask import json
import time
from app import app
from app.tests.v1.common_requests import CommonRequests
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class PasswordChangeTestCase(CommonRequests):
    """This class represents the shopping list test case"""

    def setUp(self):
        self.set_up_tests()
        CommonRequests.set_up_user_account(self)

    def test_invalid_token_provided(self):
        """Test API can create a shopping list (POST request)"""

        with app.test_client() as client:

            result = self.password_reset(
                client, "token", {})

            self.assertEqual(result.status_code, 400)
            self.assertIn("error", json.loads(result.data))

    def test_valid_but_expired_token_provided(self):
        """Test API can create a shopping list (POST request)"""

        with app.test_client() as client:
            s = Serializer(app.config['SECRET_KEY'], expires_in=1)
            tok = s.dumps({'email': CommonRequests.sign_up_credentials["email"]})

            # wait for the token to expire
            time.sleep(3)

            result = self.password_reset(
                client, str(tok.decode("utf-8")), {})

            print( result.data )
            self.assertEqual(result.status_code, 401)
            self.assertIn("error", json.loads(result.data))

    def test_valid_token_provided_password_required(self):
        """Test API can create a shopping list (POST request)"""

        with app.test_client() as client:
            s = Serializer(app.config['SECRET_KEY'], expires_in=60)
            tok = s.dumps({'email': CommonRequests.sign_up_credentials["email"]})

            self.password_change["password"] = ''
            result = self.password_reset(
                client, str(tok.decode("utf-8")), self.password_change)

            self.assertEqual(result.status_code, 200)
            self.assertIn("error", json.loads(result.data))

    def test_valid_token_provided_password_confirm_required(self):
        """Test API can create a shopping list (POST request)"""

        with app.test_client() as client:
            s = Serializer(app.config['SECRET_KEY'], expires_in=60)
            tok = s.dumps({'email': CommonRequests.sign_up_credentials["email"]})

            self.password_change["password_confirm"] = ''
            result = self.password_reset(
                client, str(tok.decode("utf-8")), self.password_change)

            self.assertEqual(result.status_code, 200)
            self.assertIn("error", json.loads(result.data))


    def test_valid_token_provided_password_reset(self):
        """Test API can create a shopping list (POST request)"""

        with app.test_client() as client:
            s = Serializer(app.config['SECRET_KEY'], expires_in=60)
            tok = s.dumps({'email': CommonRequests.sign_up_credentials["email"]})

            self.password_change["password"] = 'aa'
            self.password_change["password_confirm"] = 'aa'
            result = self.password_reset(
                client, str(tok.decode("utf-8")), self.password_change)

            self.assertEqual(result.status_code, 200)
            self.assertIn("success", json.loads(result.data))
