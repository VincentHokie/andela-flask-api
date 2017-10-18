
from app.tests.v1.common_requests import CommonRequests


class CommonRequestsv2(CommonRequests):

    # crud on a shopping list items
    def get_single_shopping_list(self, client, list_id):
        return client.get('/v2/shoppinglists/'+str(list_id),
                          headers=self.get_auth_header())

    def get_single_shopping_list_item(self, client, list_id, item_id):
        return client.get('/v2/shoppinglists/'+str(list_id)+"/items/"+str(item_id),
                          headers=self.get_auth_header())

    def get_all_shopping_list_items(self, client, list_id, search=""):
        if search and search.strip() != "":
            search = "?q="+search
        else:
            search = ""

        return client.get('/v2/shoppinglists/'+str(list_id)+"/items"+search,
                          headers=self.get_auth_header())
