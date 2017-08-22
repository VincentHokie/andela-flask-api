
from app.views import app, is_testing
from app.models import db, ShoppingList
from datetime import datetime
from app.tests.common_requests import CommonRequests


class ShoppingListTestCase(CommonRequests):
    """This class represents the shopping list test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        is_testing()
        self.app = app
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

        self.sign_up(self.sign_up_credentials)
        self.login(self.login_credentials)

        shopping_list = {'name': 'vince'}
        res = self.create_shopping_list(shopping_list)
        the_list = ShoppingList.query.filter_by(name=shopping_list["name"]).first()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(the_list.name, shopping_list["name"])
        self.assertGreater(datetime.now(), the_list.date)

    def test_shopping_list_name_required(self):
        """Test API can create a shopping list (POST request)"""

        self.sign_up(self.sign_up_credentials)
        self.login(self.login_credentials)

        shopping_list = {'name': ''}
        res = self.create_shopping_list(shopping_list)

        self.assertEqual(res.status_code, 200)
        self.assertIn("error", res.data)

    def test_api_can_get_all_shopping_lists(self):
        """Test API can get shopping lists (GET request)."""

        self.sign_up(self.sign_up_credentials)
        self.login(self.login_credentials)

        res = self.get_all_shopping_list()
        self.assertEqual(res.status_code, 200)

    def test_api_can_update_shopping_list(self):
        """Test API can get a single bucketlist by using it's id."""

        self.sign_up(self.sign_up_credentials)
        self.login(self.login_credentials)

        shopping_list = {'name': 'vince'}
        shopping_list_updated = {'name': 'vince123'}

        self.create_shopping_list(shopping_list)
        the_list = ShoppingList.query.filter_by(name=shopping_list["name"]).first()

        rv = self.update_shopping_list(shopping_list_updated, the_list.list_id)

        the_list = ShoppingList.query.filter_by(list_id=the_list.list_id).first()

        self.assertEqual(rv.status_code, 200)
        self.assertEqual(shopping_list_updated["name"], the_list.name)

    def test_api_can_delete_shopping_list(self):
        """Test API can get a single bucketlist by using it's id."""

        self.sign_up(self.sign_up_credentials)
        self.login(self.login_credentials)

        shopping_list = {'name': 'vince'}
        self.create_shopping_list(shopping_list)

        the_list = ShoppingList.query.filter_by(name=shopping_list["name"]).first()
        result = self.delete_shopping_list(the_list.list_id)

        count = db.session.query(ShoppingList).filter(list_id=the_list.list_id).count()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(0, count)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()