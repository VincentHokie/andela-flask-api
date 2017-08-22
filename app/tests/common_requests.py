
import unittest

class CommonRequests(unittest.TestCase):

    # authentication methods
    def login(self, login_credentials):
        return self.client().post('/auth/login', data=login_credentials)

    def sign_up(self, sign_up_credentials):
        return self.client().post('/auth/register', data=sign_up_credentials)

    def logout(self):
        return self.client().get('/auth/logout')


    # crud on a shopping list
    def get_all_shopping_list(self):
        return self.client().get('/shoppinglists')

    def create_shopping_list(self, shopping_list):
        return self.client().post('/shoppinglists', data=shopping_list)

    def update_shopping_list(self, shopping_list, list_id):
        return self.client().put('/shoppinglists/'+list_id,
                                 data=shopping_list,
                                 headers={'Content-Type': 'application/x-www-form-urlencoded'})

    def delete_shopping_list(self, list_id):
        return self.client().delete('/shoppinglists/'+list_id,
                                    headers={'Content-Type': 'application/x-www-form-urlencoded'})


    # crud on a shopping list items
    def get_items_under_shopping_list(self, list_id):
        return self.client().get('/shoppinglists/'+list_id)

    def create_shopping_list_item(self, shopping_list_item, list_id):
        return self.client().post('/shoppinglists/'+list_id+'/items', data=shopping_list_item)

    def update_shopping_list_item(self, shopping_list_item, list_id, item_id):
        return self.client().put('/shoppinglists/'+list_id+'/items'+item_id,
                                 data=shopping_list_item,
                                 headers={'Content-Type': 'application/x-www-form-urlencoded'})

    def delete_shopping_list_item(self, list_id, item_id):
        return self.client().delete('/shoppinglists/'+list_id+'/items'+item_id,
                                    headers={'Content-Type': 'application/x-www-form-urlencoded'})