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


@app.route("/v2/shoppinglists/<id>", methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def shopping_list_id_v2(id):

    response = jsonify(
        {
            "error":
                "Something went wrong with your delete please try again"
        })
    response.status_code = 200
    return response
