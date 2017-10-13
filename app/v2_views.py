import sys
from pathlib import Path # if you haven't already done so
from flask import render_template, request, jsonify, session
from app import app, auth

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

# Additionally remove the current file's directory from sys.path
try:
    sys.path.remove(str(parent))
except ValueError: # Already removed
    pass

from app.models import db, User, ShoppingListItem, ShoppingList
from app.forms import LoginForm, SignUpForm, ShoppingListForm, \
    ShoppingListItemForm, EmailForm, PasswordResetForm

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


@app.route("/v2/documentation", methods=['GET'])
def index_v2():
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
