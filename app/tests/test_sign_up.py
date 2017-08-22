
import unittest

from app.views import app, is_testing
from app.models import db

from app.models import User, ShoppingList, ShoppingListItem

class SignUpTestCase(unittest.TestCase):
    """This class represents the sign up test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        is_testing()
        self.app = app
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_sign_up(self):
        """Test API can create a user (POST request)"""

        sign_up_credentials = {'username': 'vince', "email": "vincenthokie@gmail.com", "password": "123",
                                    "password2": "123"}
        res = self.sign_up(sign_up_credentials)

        count = db.session.query(User).filter(username=sign_up_credentials["username"]).count()
        self.assertEqual(1, count)
        self.assertEqual(res.status_code, 201)


    def test_sign_up_password_confirmation(self):
        """Test API can notice incorrect password confirmation (POST request)"""

        sign_up_credentials = {'username': 'vince2', "email": "vincenthokie@gmail.com", "password": "123",
                               "password2": "1233"}

        res = self.sign_up(sign_up_credentials)
        count = db.session.query(User).filter(username=sign_up_credentials["username"]).count()
        self.assertEqual(0, count)
        self.assertEqual(res.status_code, 200)
        self.assertIn("error", res.data)

    def test_sign_up_email_required(self):
        """Test API can notice email is required (GET request)."""

        sign_up_credentials = {"username" : "vince3", "email": "", "password": "123",
                               "password2": "123"}
        res = self.sign_up(sign_up_credentials)

        count = db.session.query(User).filter(username=sign_up_credentials["username"]).count()
        self.assertEqual(0, count)
        self.assertEqual(res.status_code, 200)
        self.assertIn("error", res.data)

    def test_sign_up_password_required(self):
        """Test API can notice password is required (GET request)."""

        sign_up_credentials = {"username" : "vince4", "email": "vincenthokie@gmail.com", "password": "",
                               "password2": "123"}
        res = self.sign_up(sign_up_credentials)

        count = db.session.query(User).filter(username=sign_up_credentials["username"]).count()
        self.assertEqual(0, count)
        self.assertEqual(res.status_code, 200)
        self.assertIn("error", res.data)

    def test_sign_up_username_required(self):
        """Test API can notice username is required (GET request)."""

        sign_up_credentials = {"username" : "", "email": "vincenthokie@gmail.com", "password": "123",
                               "password2": "123"}
        res = self.sign_up(sign_up_credentials)

        count = db.session.query(User).filter(email=sign_up_credentials["email"]).count()
        self.assertEqual(0, count)
        self.assertEqual(res.status_code, 200)
        self.assertIn("error", res.data)

    def test_sign_up_password_confirm_required(self):
        """Test API can notice password is required (GET request)."""

        sign_up_credentials = {"username" : "vince5", "email": "vincenthokie@gmail.com", "password": "123",
                               "password2": ""}
        res = self.sign_up(sign_up_credentials)

        count = db.session.query(User).filter(username=sign_up_credentials["username"]).count()
        self.assertEqual(0, count)
        self.assertEqual(res.status_code, 200)
        self.assertIn("error", res.data)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()