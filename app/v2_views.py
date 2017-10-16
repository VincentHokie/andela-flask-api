'''
    This module is version 2 of the v1_views routes containing API ugrades
'''
import sys
from pathlib import Path  # if you haven't already done so
from flask import render_template, jsonify, session
from app import app, auth
from app.v1_views import check_list_exists, check_valid_list_id, ShoppingList

FILE = Path(__file__).resolve()
PARENT, ROOT = FILE.parent, FILE.parents[1]
sys.path.append(str(ROOT))

# Additionally remove the current file's directory from sys.path
try:
    sys.path.remove(str(PARENT))
except ValueError:  # Already removed
    pass


@app.route("/v2/documentation", methods=['GET'])
def index_v2():
    '''
        get the documentation of the new features implemented in v2 of the API
    '''
    return render_template("index.html")


@app.route("/v2/shoppinglists/<list_id>", methods=['GET'])
@auth.login_required
def get_shopping_list_v2(list_id):
    '''
        route upgrade, RESTfully get a single shoppping list
    '''
    # ensure id is a valid integer
    is_valid = check_valid_list_id(list_id)
    if is_valid is not None:
        return is_valid

    # ensure our list actually exists
    lists = check_list_exists(ShoppingList.query.filter_by(
        list_id=list_id, user_id=session["user"]).first(), list_id)
    if not isinstance(lists, ShoppingList):
        return lists

    # retrieve and send back the needed information
    response = jsonify(
        ShoppingList.query.filter_by(list_id=list_id).first().serialize
        )

    response.status_code = 200
    return response
