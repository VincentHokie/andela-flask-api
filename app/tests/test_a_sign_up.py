
import unittest

import pytest
from flask import json
from app.views import app
from app.models import db

from app.models import User, ShoppingList, ShoppingListItem

from app.tests.common_requests import CommonRequests

class SignUpTestCase(CommonRequests):
    """This class represents the sign up test case"""

    @pytest.mark.first
    def test_sign_up(self):
        """Test API can create a user (POST request)"""

        with app.test_client() as client:
            res = self.sign_up(client, self.sign_up_credentials)

            self.assertNotEqual(User.query.filter_by(
                username=self.sign_up_credentials["username"]).first(), None)
            self.assertEqual(res.status_code, 201)

    def test_duplicate_username(self):
        """Test API can create a user (POST request)"""

        with app.test_client() as client:
            res = self.sign_up(client, self.sign_up_credentials)
            resp = json.loads(res.data)

            self.assertIn("error", resp)
            self.assertEqual(res.status_code, 200)

    def test_duplicate_email(self):
        """Test API can create a user (POST request)"""

        sign_up_credentials = {
            'username': 'vincex', "email": "vincenthokie@gmail.com",
            "password": "123", "password2": "123"}

        with app.test_client() as client:
            res = self.sign_up(client, sign_up_credentials)
            resp = json.loads(res.data)
            print( resp )

            self.assertIn("error", resp)
            self.assertEqual(res.status_code, 200)

    def test_sign_up_password_confirmation(self):
        """Test API can notice incorrect password confirmation (POST request)"""

        sign_up_credentials = {
            'username': 'vince2', "email": "vincenthokiee@gmail.com",
            "password": "123", "password2": "1233"}

        with app.test_client() as client:
            res = self.sign_up(client, sign_up_credentials)

            self.assertEqual(User.query.filter_by(
                username=sign_up_credentials["username"]).first(), None)
            self.assertEqual(res.status_code, 200)
            self.assertIn("error", json.loads(res.data))

    def test_sign_up_email_required(self):
        """Test API can notice email is required (GET request)."""

        sign_up_credentials = {"username": "vince3", "email": "",
                               "password": "123", "password2": "123"}

        with app.test_client() as client:
            res = self.sign_up(client, sign_up_credentials)

            self.assertEqual(User.query.filter_by(
                username=sign_up_credentials["username"]).first(), None)
            self.assertEqual(res.status_code, 200)
            self.assertIn("error", json.loads(res.data))

    def test_sign_up_password_required(self):
        """Test API can notice password is required (GET request)."""

        sign_up_credentials = {
            "username": "vince4", "email": "vincenthokie@gmail.com",
            "password": "", "password2": "123"}

        with app.test_client() as client:
            res = self.sign_up(client, sign_up_credentials)

            self.assertEqual(User.query.filter_by(
                username=sign_up_credentials["username"]).first(), None)
            self.assertEqual(res.status_code, 200)
            self.assertIn("error", json.loads(res.data))

    def test_sign_up_username_required(self):
        """Test API can notice username is required (GET request)."""

        sign_up_credentials = {
            "username": "", "email": "vincenthokie1@gmail.com",
            "password": "123", "password2": "123"}

        with app.test_client() as client:
            res = self.sign_up(client, sign_up_credentials)

            self.assertEqual(User.query.filter_by(
                email=sign_up_credentials["email"]).first(), None)
            self.assertEqual(res.status_code, 200)
            self.assertIn("error", json.loads(res.data))

    def test_sign_up_password_confirm_required(self):
        """Test API can notice password is required (GET request)."""

        sign_up_credentials = {
            "username": "vince5", "email": "vincenthokie@gmail.com",
            "password": "123", "password2": ""}

        with app.test_client() as client:
            res = self.sign_up(client, sign_up_credentials)

            self.assertEqual(User.query.filter_by(
                username=sign_up_credentials["username"]).first(), None)
            self.assertEqual(res.status_code, 200)
            self.assertIn("error", json.loads(res.data))

    def tearDown(self):
        return False