
from flask import json

from app.views import app
from app.models import db, ShoppingList
from datetime import datetime
from app.tests.common_requests import CommonRequests


class ShoppingListTestCase(CommonRequests):
    """This class represents the shopping list test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        POSTGRES = {
            'user': 'vince',
            'pw': 'vince',
            'db': 'test_db',
            'host': 'localhost',
            'port': '5432',
        }

        app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

        self.client = self.app.test_client
        self.sign_up_credentials = {'username': 'vince', "email": "vincenthokie@gmail.com", "password": "123",
                                    "password2": "123"}
        self.login_credentials = {'username': 'vince', "password": "123"}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_shopping_list_creation(self):
        """Test API can create a shopping list (POST request)"""

        with app.test_client() as client:
            self.sign_up(client, self.sign_up_credentials)
            self.login(client, self.login_credentials)

            shopping_list = {'name': 'vince'}
            res = self.create_shopping_list(client, shopping_list, self.login_credentials)
            print(res.data)
            back_data = json.loads(res.data)

            self.assertEqual(res.status_code, 201)
            self.assertEqual(back_data['name'], shopping_list["name"])
            # self.assertGreater(
            #    datetime.now().strftime("%Y-%b-%d %H:%M:%-S"),
            #    datetime.strptime(back_data['date'][0]+" "+back_data['date'][1], "%Y-%b-%d %H:%M:%-S")
            # )



    def test_shopping_list_name_required(self):
        """Test API can create a shopping list (POST request)"""

        with app.test_client() as client:
            self.sign_up(client, self.sign_up_credentials)
            self.login(client, self.login_credentials)

            shopping_list = {'name': ''}
            res = self.create_shopping_list(client, shopping_list, self.login_credentials)
            back_data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertIn("error", back_data)



    def test_api_can_get_all_shopping_lists(self):
        """Test API can get shopping lists (GET request)."""

        with app.test_client() as client:
            self.sign_up(client, self.sign_up_credentials)
            self.login(client, self.login_credentials)

            shopping_list = {'name': ''}
            self.create_shopping_list(client, shopping_list, self.login_credentials)

            res = self.get_all_shopping_list(client, self.login_credentials)

            self.assertEqual(res.status_code, 200)




    def test_api_can_update_shopping_list(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:
            self.sign_up(client, self.sign_up_credentials)
            self.login(client, self.login_credentials)

            shopping_list = {'name': 'vince'}
            shopping_list_updated = {'name': 'vince123'}
            res = self.create_shopping_list(client, shopping_list, self.login_credentials)
            the_list = json.loads(res.data)

            res = self.update_shopping_list(client, shopping_list_updated, the_list['list_id'], self.login_credentials)
            the_list = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertIn("success", the_list)


    def test_api_can_delete_shopping_list(self):
        """Test API can get a single bucketlist by using it's id."""

        with app.test_client() as client:
            self.sign_up(client, self.sign_up_credentials)
            self.login(client, self.login_credentials)

            shopping_list = {'name': 'vince'}
            res = self.create_shopping_list(client, shopping_list, self.login_credentials)
            the_list = json.loads(res.data)

            result = self.delete_shopping_list(client, the_list['list_id'], self.login_credentials)

            self.assertEqual(result.status_code, 202)
            self.assertIn("success", json.loads(result.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()