
import unittest
from base64 import b64encode

class CommonRequests(unittest.TestCase):


    def define_db_connections(self, app):
        POSTGRES = {
            'user': 'vince',
            'pw': 'vince',
            'db': 'test_db',
            'host': 'localhost',
            'port': '5432',
        }

        app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

    # authentication methods
    def login(self, client,  login_credentials):
        return client.post('/auth/login', data=login_credentials)

    def sign_up(self, client, sign_up_credentials):
        return client.post('/auth/register', data=sign_up_credentials)

    def logout(self, client):
        return client.get('/auth/logout')

    def get_auth_header(self, username, password):
        return {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic %s' % b64encode(
                bytes(username + ':' + password, "utf-8")).decode("ascii")
        }

    # crud on a shopping list
    def get_all_shopping_list(self, client, credentials):
        return client.get('/shoppinglists',
                          headers=self.get_auth_header(credentials["username"], credentials['password']))

    def create_shopping_list(self, client,  shopping_list, credentials):
        return client.post('/shoppinglists', data=shopping_list,
                           headers=self.get_auth_header(credentials["username"], credentials['password']))

    def update_shopping_list(self, client,  shopping_list, list_id, credentials):
        headers=self.get_auth_header(credentials["username"], credentials['password'])
        headers["Content-Type"] = 'application/x-www-form-urlencoded'
        return client.put('/shoppinglists/'+str(list_id),
                                 data=shopping_list,
                                 headers=headers)

    def delete_shopping_list(self, client, list_id, credentials):
        headers = self.get_auth_header(credentials["username"], credentials['password'])
        headers["Content-Type"] = 'application/x-www-form-urlencoded'
        return client.delete('/shoppinglists/'+str(list_id),
                                    headers=headers)


    # crud on a shopping list items
    def get_items_under_shopping_list(self, client, list_id, credentials):
        return client.get('/shoppinglists/'+str(list_id),
                           headers=self.get_auth_header(credentials["username"], credentials['password']))

    def create_shopping_list_item(self, client, shopping_list_item, list_id, credentials):
        return client.post('/shoppinglists/'+str(list_id)+'/items', data=shopping_list_item,
                           headers=self.get_auth_header(credentials["username"], credentials['password']))

    def update_shopping_list_item(self, client, shopping_list_item, list_id, item_id, credentials):
        return client.put('/shoppinglists/'+str(list_id)+'/items/'+str(item_id),
                                 data=shopping_list_item,
                                 headers=self.get_auth_header(credentials["username"], credentials['password']))

    def delete_shopping_list_item(self, client, list_id, item_id, credentials):
        return client.delete('/shoppinglists/'+str(list_id)+'/items/'+str(item_id),
                                    headers=self.get_auth_header(credentials["username"], credentials['password']))