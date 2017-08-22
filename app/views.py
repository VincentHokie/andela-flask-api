
import os
from flask import Flask
from flask import render_template, request, jsonify, g
from models import db, User, ShoppingListItem, ShoppingList
from forms import LoginForm, SignUpForm, ShoppingListForm, ShoppingListItemForm

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["DEBUG"] = True
app.config["CSRF_ENABLED"] = True

POSTGRES = {
    'user': 'vince',
    'pw': 'vince',
    'db': 'andela-flask-api',
    'host': 'localhost',
    'port': '5432',
}

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# make wft extension consider cross-site request forgery
app.config["WTF_CSRF_ENABLED"] = True

# required when the above config is enabled, this will be used to
# generate a scrf token..should be a string that cant be easily
# guessed in production
app.config["SECRET_KEY"] = 'youll-never-know-what-it-is-coz-its-secret'

db.init_app(app)

def is_testing():
    POSTGRES["db"] = 'test_db'
    app.config["TESTING"] = True




@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route("/auth/register", methods=['GET'])
def register():
    if request.method == "POST":
        form = SignUpForm()
        if form.validate_on_submit():
            return render_template("index.html",
                               title='Home')
        else:
            return {"error" : ""}

@app.route("/auth/login", methods=['POST'])
def login():
    if request.method == "POST":
        form = LoginForm()
        if form.validate_on_submit():
            return render_template("index.html",
                               title='Home')
        else:
            return {"error" : ""}

@app.route("/auth/logout", methods=['POST'])
def logout():
    if request.method == "POST":

        return render_template("index.html",
                               title='Home')

@app.route("/auth/reset-password", methods=['GET', 'POST'])
def reset_password():
    if request.method == "POST":

        return render_template("index.html",
                               title='Home')





@app.route("/shoppinglists", methods=['GET', 'POST'])
@auth.login_required
def shopping_lists():
    if request.method == "POST":
        form = ShoppingList()
        if form.validate_on_submit():
            return render_template("index.html",
                                   title='Home')
        else:
            return {"error": ""}
    elif request.method == "GET":

        return render_template("index.html",
                               title='Home')

@app.route("/shoppinglists/<id>", methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def shopping_list_id():
    if request.method == "GET":

        return render_template("index.html",
                               title='Home')
    elif request.method == "PUT":
        form = LoginForm()
        if form.validate_on_submit():

            admin = ShoppingList.query.filter_by(username='admin').first()
            admin.email = 'my_new_email@example.com'
            db.session.commit()

            return render_template("index.html",
                                   title='Home')
        else:
            return {"error": ""}

    elif request.method == "DELETE":


        return render_template("index.html",
                               title='Home')



@app.route("/shoppinglists/<id>/items", methods=['POST'])
@auth.login_required
def shopping_list_items():
    if request.method == "POST":

        return render_template("index.html",
                               title='Home')

@app.route("/shoppinglists/<id>/items/<item_id>", methods=['PUT', 'DELETE'])
@auth.login_required
def shopping_list_item_update():
    if request.method == "PUT":
        admin = ShoppingListItem.query.filter_by(username='admin').first()
        admin.email = 'my_new_email@example.com'
        db.session.commit()

        return render_template("index.html",
                               title='Home')
    elif request.method == "DELETE":

        return render_template("index.html",
                               title='Home')


@app.route('/api/token', methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })


if __name__ == '__main__':
    app.run(debug=True)