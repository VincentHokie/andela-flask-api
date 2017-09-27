
import os
import base64
from flask import Flask
from flask import render_template, request, jsonify, session, url_for

try:
    from .models import db, User, ShoppingListItem, ShoppingList
    from .forms import LoginForm, SignUpForm, ShoppingListForm, \
        ShoppingListItemForm, EmailForm, PasswordResetForm
except ImportError:
    from models import db, User, ShoppingListItem, ShoppingList
    from forms import LoginForm, SignUpForm, ShoppingListForm, \
        ShoppingListItemForm, EmailForm, PasswordResetForm

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from flask_mail import Mail, Message

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


if os.environ.get("HEROKU_POSTGRESQL_CRIMSON_URL") is None:
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://%(user)s:\
        %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        os.environ['HEROKU_POSTGRESQL_CRIMSON_URL']

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# make wft extension consider cross-site request forgery
app.config["WTF_CSRF_ENABLED"] = False

# required when the above config is enabled, this will be used to
# generate a scrf token..should be a string that cant be easily
# guessed in production
app.config["SECRET_KEY"] = 'youll-never-know-what-it-is-coz-its-secret'

# email server
app.config["MAIL_SERVER"] = 'smtp.googlemail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "andelatestmail"
app.config["MAIL_PASSWORD"] = "andelatestmail1"
app.config["MAIL_DEFAULT_SENDER"] = "andelatestmail@gmail.com"

# administrator list
ADMINS = ['your-gmail-username@gmail.com']

db.init_app(app)
mail = Mail(app)


# helper function for sending user emails
def send_email(subject, recipients, text_body, html_body=None):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def check_valid_list_id(list_id):
    try:
        int(list_id)
    except:
        response = jsonify(
            {
                "error":
                    "Shopping list id: " + list_id + " is not a valid id!"
            })
        response.status_code = 500
        return response

    return None


def check_valid_item_id(item_id):
    try:
        int(item_id)
    except:
        response = jsonify(
            {
                "error":
                    "Shopping list item id: " + item_id + " is not a valid id!"
            })
        response.status_code = 500
        return response

    return None


def check_list_exists(the_list, list_id):

    if the_list is None:
        response = jsonify(
            {
                "error":
                    "Shopping list with id: " + list_id + " is not found!"
            })
        response.status_code = 404
        return response

    return the_list


def check_item_exists(the_item, item_id):

    if the_item is None:
        response = jsonify(
            {
                "error":
                    "Shopping list item with id: " + item_id + " not found!"
            })
        response.status_code = 404
        return response

    return the_item


# function used to verify whether username/password or token provided are valid
@auth.verify_password
def verify_password(username_or_token, password=None):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False

    if user.token != username_or_token:
        user.invalidate_token()
        return False

    session["user"] = user.user_id
    return True


# decorator used to allow cross origin requests
@app.after_request
def apply_cross_origin_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'

    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET,HEAD,OPTIONS," \
                                                       "POST,PUT,DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Access-Control-Allow-" \
        "Headers, Origin,Accept, X-Requested-With, Content-Type, " \
        "Access-Control-Request-Method, Access-Control-Request-Headers," \
        "Access-Control-Allow-Origin, Authorization"

    return response

@app.route("/documentation", methods=['GET'])
def index():
    return render_template("index.html")


@app.route("/auth/register", methods=['POST'])
def register():

    form = SignUpForm()
    # the form has been properly filled in
    if form.validate_on_submit():

        user = User(
            form.email.data,
            form.username.data,
            form.password.data
        )

        # ensure the username is unique, otherwise return an error
        if User.query.filter_by(username=form.username.data).first() \
                is not None:
            response = jsonify(
                {
                    "error":
                        {
                            "username": ["This username is not unique, please "
                                         "select another"]
                        }
                })
            response.status_code = 200
            return response

        # ensure the email is unique, otherwise return an error
        if User.query.filter_by(email=form.email.data).first() is not None:
            response = jsonify(
                {
                    "error":
                        {
                            "email":
                                [
                                    "This email is not unique, please "
                                    "select another"
                                ]
                        }
                })
            response.status_code = 200
            return response

        # try and save the user, if anything goes wrong..
        # send back an error message
        try:
            user.save()
        except:
            response = jsonify(
                {
                    "error":
                        "Something went wrong, please try again"
                })
            response.status_code = 200
            return response

        # if were here, the save worked..return a success message
        take_back = {"success": "Sign up successful, login to continue!"}
        response = jsonify(take_back)
        response.status_code = 201
        return response

    # the form was not properly filled
    else:
        response = jsonify({"error": form.errors})
        response.status_code = 200
        return response


@app.route("/auth/login", methods=['POST'])
def login():
    if request.method == "POST":
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()

            take_back = {"success": "You have successfully logged in"}

            if not user or not user.verify_password(form.password.data):
                take_back = {
                    "error":
                    "Login failed! Your credentials don't match our records"
                }
            else:
                token = user.generate_auth_token()
                take_back['token'] = token.decode('ascii')
                user.save_token(token.decode('ascii'))
                session["user"] = user.user_id

            response = jsonify(take_back)
            response.status_code = 200
            return response

        else:
            response = jsonify({"error": form.errors})
            response.status_code = 200
            return response


@app.route("/auth/logout", methods=['POST'])
@auth.login_required
def logout():
    if request.method == "POST":
        user = User.query.filter_by(user_id=session["user"]).first()
        if user is not None:
            user.invalidate_token()
            session.pop('user', None)
            response = jsonify({"success": "You have successfully logged out!"})
            response.status_code = 200
            return response


@app.route('/auth/reset-password', methods=['POST'])
@app.route("/auth/reset-password/<token>", methods=['POST'])
def reset_password(token=None):

    # ensure its a post request
    if request.method == "POST":

        # the user is trying to update the password and
        # has submitted the passwords
        if token is not None:

            s = Serializer(app.config['SECRET_KEY'])

            # check if the token is a valid one and return a useful message
            try:
                data = s.loads(token)
            except SignatureExpired:
                # valid token, but expired
                response = jsonify(
                    {
                        "error":
                        "Your link expired, request another and use that!"
                    })
                response.status_code = 401
                return response
            except BadSignature:
                # invalid token
                response = jsonify({"error": "Nice try.."})
                response.status_code = 404
                return response

            # if were here, we've fount that the token is valid
            form = PasswordResetForm()
            email = data['email']

            # the passwords have been properly filled in the form
            if form.validate_on_submit():

                # ensure the user from the token exists
                user = User.query.filter_by(email=email).first()

                # user doesnt exist for some reason
                if user is None:
                    response = jsonify(
                        {
                            "error":
                                "You're not in our pool of users!"
                        })
                    response.status_code = 404
                    return response

                # user exists and we can update their password
                user.password = user.hash_password(form.password.data)
                db.session.commit()

                # send a success message back
                response = jsonify(
                    {
                        "success":
                            "Your password has been successfully reset,"
                            " you can use it to log in now"
                    })
                response.status_code = 200
                return response

            # the form wasnt properly submitted, return error messages
            else:
                response = jsonify({"error": form.errors})
                response.status_code = 200
                return response

        # there is no token, so we should be receiving the user email
        else:

            form = EmailForm()

            # the email has been properly submitted
            if form.validate_on_submit():

                # retrieve user and check if they exist
                user = User.query.filter_by(email=form.email.data).first()

                # user does not exist
                if user is None:
                    response = jsonify(
                        {
                            "error":
                                "You're not in our pool of users!"
                        })
                    response.status_code = 404
                    return response

                # user exists, make a token from the secret key and
                # a dictionary of the users email
                s = Serializer(app.config['SECRET_KEY'], expires_in=600)
                tok = s.dumps({'email': form.email.data})

                # create a url and send it in the email
                password_reset_url = \
                    "https://andela-react-client.herokuapp.com/" \
                    "password-reset/"+str(tok.decode("utf-8"))

                email_body = "Please follow this link to reset your " \
                             "password\n\n"+password_reset_url+"\n\n If you're " \
                             "not the one who requested this, please ignore " \
                             "this and contact the administrator about this."

                send_email(
                    'Password Reset Requested', [form.email.data], email_body)

                # return a success message
                response = jsonify(
                    {
                        "success":
                            "An email has been sent to you with a link you "
                            "can use to reset your password"
                    })
                response.status_code = 200
                return response

            # the form was not properly submitted, return error messages
            else:
                response = jsonify({"error": form.errors})
                response.status_code = 200
                return response


@app.route("/shoppinglists", methods=['GET', 'POST'])
@auth.login_required
def shopping_lists():

    # were adding a shopping list
    if request.method == "POST":
        form = ShoppingListForm()

        # the form was properly filled
        if form.validate_on_submit():

            # create the list
            list = ShoppingList(form.name.data, session["user"])
            list.save()

            # retrieve the list and send it back to the user
            list = ShoppingList.query.filter_by(
                name=form.name.data, user_id=session["user"]).first()
            response = jsonify(list.serialize)
            response.status_code = 201
            return response

        # the form was not properly filled, return an error message
        else:
            response = jsonify({"error": form.errors})
            response.status_code = 200
            return response

    # we want to see all the shopping lists
    elif request.method == "GET":

        list_id = request.args.get("list_id")
        if list_id is not None:

            # ensure id is a valid integer
            is_valid = check_valid_list_id(list_id)
            if is_valid is not None:
                return is_valid

            gotten_list = ShoppingList.query.filter_by(
                list_id=list_id, user_id=session["user"]).first()

            gotten_list = check_list_exists(gotten_list, id)
            if not isinstance(gotten_list, ShoppingList):
                return gotten_list

            # get the list requested for only
            response = jsonify(gotten_list.serialize)

        else:
            # get all the lists and send them to the user
            response = jsonify(
                [i.serialize for i in ShoppingList.get_all(
                    session["user"],
                    request.args.get("q"),
                    request.args.get("limit"))])

        response.status_code = 200
        return response


@app.route("/shoppinglists/items", methods=['GET'])
@auth.login_required
def all_shopping_list_items():

    item_id = request.args.get("item_id")
    if item_id is not None:

        # ensure id is a valid integer
        is_valid = check_valid_item_id(item_id)
        if is_valid is not None:
            return is_valid

        gotten_item = ShoppingListItem.query\
            .join(ShoppingList)\
            .filter(ShoppingList.user_id == session["user"])\
            .filter(ShoppingListItem.item_id == item_id)\
            .first()

        gotten_item = check_item_exists(gotten_item, id)
        if not isinstance(gotten_item, ShoppingListItem):
            return gotten_item

        # get the list requested for only
        response = jsonify(gotten_item.serialize)

    else:
        # get all the list items and send them to the user
        response = jsonify(
            [
                i.serialize for i in ShoppingListItem.
                get_all_despite_list(session["user"])
            ])

    response.status_code = 200
    return response


@app.route("/shoppinglists/<id>", methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def shopping_list_id(id):

    # ensure id is a valid integer
    is_valid = check_valid_list_id(id)
    if is_valid is not None:
        return is_valid

    # ensure our list actually exists
    lists = check_list_exists(ShoppingList.query.filter_by(
        list_id=id, user_id=session["user"]).first(), id)
    if not isinstance(lists, ShoppingList):
        return lists

    # we want all the items under the list with the given id
    if request.method == "GET":

        # retrieve and send back the needed information
        response = jsonify([
                               i.serialize for i in ShoppingListItem.get_all(
                id, request.args.get("q"), request.args.get("limit"))
                               ])
        response.status_code = 200
        return response

    # were updating a list
    elif request.method == "PUT":
        form = ShoppingListForm()

        # the form was properly filled
        if form.validate_on_submit():

            # update the list
            lists.name = form.name.data
            db.session.commit()

            # send the user a meaningful response
            response = jsonify({"success": "Shopping list update successful!"})
            response.status_code = 200
            return response

        # the form was not properly filled
        else:
            response = jsonify({"error": form.errors})
            response.status_code = 200
            return response

    # were deleting a shopping list
    elif request.method == "DELETE":

        # delete the list, otherwise return an error
        try:
            lists.delete()
        except:
            response = jsonify(
                {
                    "error":
                        "Something went wrong with your delete please try again"
                })
            response.status_code = 200
            return response

        # if all went well, send back a success message
        response = jsonify({"success": "Shopping list delete successful!"})
        response.status_code = 202
        return response


@app.route("/shoppinglists/<id>/items", methods=['POST'])
@auth.login_required
def shopping_list_items(id):

    # were adding a new item
    if request.method == "POST":

        # ensure the provided shopping list is a valid integer
        is_valid = check_valid_list_id(id)
        if is_valid is not None:
            return is_valid

        form = ShoppingListItemForm()
        # the submitted form is of proper format
        if form.validate_on_submit():

            # the shopping list does not exist
            lists = check_list_exists(ShoppingList.query.filter_by(
                list_id=id, user_id=session["user"]).first(), id)
            if not isinstance(lists, ShoppingList):
                return lists

            # the shopping list exists, create an item object and save it
            list = ShoppingListItem(form.name.data, id, form.amount.data)
            list.save()

            # get the added item and return it to the user
            list = ShoppingListItem.query.filter_by(
                name=form.name.data, list_id=id, amount=form.amount.data
            ).first()

            response = jsonify( list.serialize )
            response.status_code = 201
            return response

        # there were form errors, return them to the user
        else:
            response = jsonify({"error": form.errors})
            response.status_code = 200
            return response


@app.route("/shoppinglists/<id>/items/<item_id>", methods=['PUT', 'DELETE'])
@auth.login_required
def shopping_list_item_update(id, item_id):

    # check if the shopping list id is indeed a valid integer
    is_valid = check_valid_list_id(id)
    if is_valid is not None:
        return is_valid

    # check if the shopping list item id is indeed a valid integer
    is_valid = check_valid_item_id(item_id)
    if is_valid is not None:
        return is_valid

    # ensure the shopping list in question exists
    lists = check_list_exists(ShoppingList.query.filter_by(
        list_id=id, user_id=session["user"]).first(), id)
    if not isinstance(lists, ShoppingList):
        return lists

    # ensure the shopping list item in question exists
    lists = ShoppingListItem.query.filter_by(
        item_id=item_id, list_id=id).first()

    lists = check_item_exists(lists, id)
    if not isinstance(lists, ShoppingListItem):
        return lists

    # were updating a shopping list item
    if request.method == "PUT":
        form = ShoppingListItemForm()
        if form.validate_on_submit():

            lists.name = form.name.data
            lists.amount = form.amount.data

            db.session.commit()

            response = jsonify({"success": "Shopping list update successful!"})
            response.status_code = 200
            return response

        # the form submitted had some validation errors
        else:
            response = jsonify({"error": form.errors})
            response.status_code = 200
            return response

    # were deleting a shopping list item
    elif request.method == "DELETE":

        lists = ShoppingListItem.query.filter_by(
            list_id=id, item_id=item_id).first()

        # delete the list item, otherwise return an error
        try:
            lists.delete()
        except:
            response = jsonify(
                {
                    "error":
                        "Something went wrong with your delete please try again"
                })
            response.status_code = 200
            return response

        response = jsonify({"success": "Shopping list delete successful!"})
        response.status_code = 202
        return response


@app.route("/shoppinglists/<id>/items/<item_id>/checkbox", methods=['PUT'])
@auth.login_required
def shopping_list_item_update(id, item_id):

    # check if the shopping list id is indeed a valid integer
    is_valid = check_valid_list_id(id)
    if is_valid is not None:
        return is_valid

    # check if the shopping list item id is indeed a valid integer
    is_valid = check_valid_item_id(item_id)
    if is_valid is not None:
        return is_valid

    # ensure the shopping list in question exists
    lists = check_list_exists(ShoppingList.query.filter_by(
        list_id=id, user_id=session["user"]).first(), id)
    if not isinstance(lists, ShoppingList):
        return lists

    # ensure the shopping list item in question exists
    lists = ShoppingListItem.query.filter_by(
        item_id=item_id, list_id=id).first()

    lists = check_item_exists(lists, id)
    if not isinstance(lists, ShoppingListItem):
        return lists

    # were updating a shopping list item bought status
    if lists.bought != 1:
        lists.bought = 1
    else:
        lists.bought = 0

	db.session.commit()

	response = jsonify({"success": "Shopping list update successful!"})
	response.status_code = 200
	return response



if __name__ == '__main__':
    app.run(debug=True)
