
from flask import json
from app.views import app
from app.models import db

from app.tests.common_requests import CommonRequests

class LoginTestCase(CommonRequests):
    """This class represents the login test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        POSTGRES = {
            'user': 'postgres',
            'pw': '',
            'db': 'testdb',
            'host': 'localhost',
            'port': '5432',
        }

        app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

        self.client = self.app.test_client

        self.sign_up_credentials = {'username': 'vince', "email": "vincenthokie@gmail.com", "password": "123",
                               "password2": "123"}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

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

    def test_token_generate(self):
        """Test API can create a token if logged in user requests it (POST request)"""

        with app.test_client() as client:
            self.sign_up(client, self.sign_up_credentials)

            login_credentials = {'username': 'vince', "password": "123"}

            headers = self.get_auth_header(login_credentials['username'],login_credentials['password'])

            res = client.get('/api/token', headers=headers)

            self.assertEqual(res.status_code, 200)
            self.assertIn("token", json.loads(res.data))


    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()