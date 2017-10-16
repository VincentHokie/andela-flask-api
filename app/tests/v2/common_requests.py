
from app.tests.v1.common_requests import CommonRequests


class CommonRequestsv2(CommonRequests):

    # crud on a shopping list items
    def get_single_shopping_list(self, client, list_id):
        return client.get('/v2/shoppinglists/'+str(list_id),
                          headers=self.get_auth_header())
