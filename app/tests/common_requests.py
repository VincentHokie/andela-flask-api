
import unittest

class CommonRequests(unittest.TestCase):

    # authentication methods
    def login(self, client,  login_credentials):
        return client.post('/auth/login', data=login_credentials)

    def sign_up(self, client, sign_up_credentials):
        return client.post('/auth/register', data=sign_up_credentials)

    def logout(self, client):
        return client.get('/auth/logout')

    def get_auth_header(self, username, password):
        return {
            'content-type': 'application/json',
            'Authorization': 'Basic %s' % b64encode(
                bytes(username + ':' + password, "utf-8")).decode("ascii")
        }

    # crud on a shopping list
    def get_all_shopping_list(self, client):
        return client.get('/shoppinglists')

    def create_shopping_list(self, client,  shopping_list):
        return client.post('/shoppinglists', data=shopping_list)

    def update_shopping_list(self, client,  shopping_list, list_id):
        return client.put('/shoppinglists/'+list_id,
                                 data=shopping_list,
                                 headers={'Content-Type': 'application/x-www-form-urlencoded'})

    def delete_shopping_list(self, client, list_id):
        return client.delete('/shoppinglists/'+list_id,
                                    headers={'Content-Type': 'application/x-www-form-urlencoded'})


    # crud on a shopping list items
    def get_items_under_shopping_list(self, client, list_id):
        return client.get('/shoppinglists/'+list_id)

    def create_shopping_list_item(self, client, shopping_list_item, list_id):
        return client.post('/shoppinglists/'+list_id+'/items', data=shopping_list_item)

    def update_shopping_list_item(self, client, shopping_list_item, list_id, item_id):
        return client.put('/shoppinglists/'+list_id+'/items'+item_id,
                                 data=shopping_list_item,
                                 headers={'Content-Type': 'application/x-www-form-urlencoded'})

    def delete_shopping_list_item(self, client, list_id, item_id):
        return client.delete('/shoppinglists/'+list_id+'/items'+item_id,
                                    headers={'Content-Type': 'application/x-www-form-urlencoded'})