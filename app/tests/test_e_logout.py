
from flask import json
from app.views import app
from app.models import db

from app.tests.common_requests import CommonRequests

class LogoutTestCase(CommonRequests):
    """This class represents the login test case"""

    def setUp(self):
        self.set_up_tests()
        self.set_up_authorized_route()

    def test_logout(self):
        """Test API can create a user (POST request)"""

        with app.test_client() as client:
            res = self.logout(client)
            self.assertEqual(res.status_code, 200)
            self.assertIn("success", json.loads(res.data))


    def tearDown(self):
        return False