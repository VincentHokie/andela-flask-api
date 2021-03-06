'''
    This module is version 2 of the v1_views routes containing API ugrades
'''
import sys
from pathlib import Path  # if you haven't already done so
from flask import render_template, jsonify, session, request
from app import app, auth
from app.v1_views import check_list_exists, check_valid_list_id, \
    ShoppingList, ShoppingListItem, check_item_exists, check_valid_item_id

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


@app.route("/v2/shoppinglists/<list_id>/items", methods=['GET'])
@auth.login_required
def shopping_list_items_v2(list_id):

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
    count = ShoppingListItem.query.filter_by(
                list_id=list_id).count()

    if request.args.get("q"):
        count = ShoppingListItem.query.filter_by(
            list_id=list_id).filter(
                ShoppingListItem.name.like(
                    "%"+request.args.get("q").strip()+"%")).count()

    response = jsonify({
        "items": [
            i.serialize for i in ShoppingListItem.get_all(
                list_id, request.args.get("q"),
                request.args.get("limit"),
                request.args.get("page"))
            ],
        "count": count
    })

    response.status_code = 200
    return response


@app.route("/v2/shoppinglists/<list_id>/items/<item_id>", methods=['GET'])
@auth.login_required
def single_shopping_list_item_v2(list_id, item_id):

    # ensure id is a valid integer
    is_valid = check_valid_list_id(list_id)
    if is_valid is not None:
        return is_valid

    # ensure our list actually exists
    lists = check_list_exists(ShoppingList.query.filter_by(
        list_id=list_id, user_id=session["user"]).first(), list_id)
    if not isinstance(lists, ShoppingList):
        return lists

    # check if the shopping list item id is indeed a valid integer
    is_valid = check_valid_item_id(item_id)
    if is_valid is not None:
        return is_valid

    # ensure the shopping list item in question exists
    lists = ShoppingListItem.query.filter_by(
        item_id=item_id, list_id=list_id).first()

    lists = check_item_exists(lists, item_id)
    if not isinstance(lists, ShoppingListItem):
        return lists

    # retrieve and send back the needed information
    response = jsonify(lists.serialize)

    response.status_code = 200
    return response
