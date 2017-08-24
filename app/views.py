
import os
from flask import Flask
from flask import render_template, request, jsonify, session, url_for
from models import db, User, ShoppingListItem, ShoppingList
from forms import LoginForm, SignUpForm, ShoppingListForm, ShoppingListItemForm, EmailForm, PasswordResetForm

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from flask_heroku import Heroku
from flask_mail import Mail, Message

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

app = Flask(__name__)
heroku = Heroku(app)

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

def is_testing():
    POSTGRES["db"] = 'test_db'
    app.config["TESTING"] = True


def send_email(subject, recipients, text_body):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    #msg.html = html_body
    mail.send(msg)



@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    session["user"] = user.user_id
    return True


@app.route("/auth/register", methods=['POST'])
def register():
    if request.method == "POST":
        form = SignUpForm()

        if form.validate_on_submit():

            if form.password.data != form.password2.data:
                take_back = {"error": "Your passwords don't match!"}

                response = jsonify(take_back)
                response.status_code = 200
                return response

            user = User(
                form.email.data,
                form.username.data,
                form.password.data
            )
            user.save()
            take_back = {"success": True}

            response = jsonify(take_back)
            response.status_code = 201
            return response

        else:
            take_back = {"error": form.errors }

            response = jsonify(take_back)
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
                take_back = {"error": "Login failed! Your credentials don't match our records"}
            else:
                session["user"] = user.user_id

            response = jsonify(take_back)
            response.status_code = 200
            return response

        else:
            take_back = {"error": form.errors}

            response = jsonify(take_back)
            response.status_code = 200
            return response

@app.route("/auth/logout", methods=['POST'])
def logout():
    if request.method == "POST":

        return render_template("index.html",
                               title='Home')

@app.route('/auth/reset-password', methods=['POST'])
@app.route("/auth/reset-password/<token>", methods=['POST'])
def reset_password(token=None):

    # ensure its a post request
    if request.method == "POST":

        # the user is trying to update the password and has submitted the passwords
        if token is not None:

            s = Serializer(app.config['SECRET_KEY'])

            # check if the token is a valid one and return a useful message
            try:
                data = s.loads(token)
            except SignatureExpired:
               # valid token, but expired
               response = jsonify({"error": "Your link expired, request another and use that!"})
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
                    response = jsonify({"error": "You're not in our pool of users!"})
                    response.status_code = 404
                    return response

                # user exists and we can update their password
                user.password = user.hash_password(form.password.data)
                db.session.commit()

                # send a success message back
                response = jsonify(
                    {"succes": "Your password has been successfully reset, you can use it to log in now"})
                response.status_code = 200
                return response

            # the form wasnt properly submitted, return error messages
            else:
                response = jsonify({"error": form.errors})
                response.status_code = 200
                return response

        # there is no token, so we should be recieving the usre email
        else:

            form = EmailForm()

            # the email has been properly submitted
            if form.validate_on_submit():

                # retrieve user and check if they exist
                user = User.query.filter_by(email=form.email.data).first()

                # user does not exist
                if user is None:
                    response = jsonify({"error": "You're not in our pool of users!"})
                    response.status_code = 404
                    return response

                # user exists, make a token from the secret key and a dictionary of the users email
                s = Serializer(app.config['SECRET_KEY'], expires_in=600)
                tok = s.dumps({'email': form.email.data})

                # create a url and send it in the email
                password_reset_url = url_for('reset_password', token=tok, _external=True)
                email_body = "Please follow this link to reset your password\n\n"+password_reset_url+"\n\n " \
                                "If you're not the one who requested this, please ignore this and contact the administrator" \
                                " about this."

                send_email('Password Reset Requested', [form.email.data], )

                # return a success message
                response = jsonify({"succes": "An email has been sent to you with a link you can use to reset your password"})
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
    if request.method == "POST":
        form = ShoppingListForm()
        if form.validate_on_submit():
            list = ShoppingList(form.name.data, session["user"])
            list.save()

            list = ShoppingList.query.filter_by(name=form.name.data, user_id=session["user"]).first()
            response = jsonify( list.serialize )
            response.status_code = 201
            return response

        else:
            response = jsonify({"error": form.errors})
            response.status_code = 200
            return response

    elif request.method == "GET":

        response = jsonify(
            [i.serialize for i in ShoppingList.get_all(
                session["user"],
                request.args.get("q"),
                request.args.get("limit"))])

        response.status_code = 200
        return response

@app.route("/shoppinglists/<id>", methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def shopping_list_id(id):
    try:
        int(id)
    except:
        response = jsonify({"error": "Shopping list id: " + id + " is not a valid id!"})
        response.status_code = 500
        return response

    if request.method == "GET":

        if ShoppingList.query.filter_by(list_id=id, user_id=session["user"]).first() is None:
            response = jsonify({"error": "Shopping list id: " + id + " is not found!"})
            response.status_code = 404
            return response

        response = jsonify(
            [i.serialize for i in ShoppingListItem.get_all(id, request.args.get("q"), request.args.get("limit"))]
        )
        response.status_code = 200
        return response

    elif request.method == "PUT":
        form = ShoppingListForm()
        if form.validate_on_submit():

            lists = ShoppingList.query.filter_by(list_id=id, user_id=session["user"]).first()

            if lists is not None:
                lists.name = form.name.data
                db.session.commit()

                response = jsonify({"success": "Shopping list update successful!"})
                response.status_code = 200
                return response

            else:
                response = jsonify({"error" : "Shopping list with id: "+id+" not found!"})
                response.status_code = 404
                return response

        else:
            response = jsonify({"error": form.errors})
            response.status_code = 200
            return response

    elif request.method == "DELETE":

        lists = ShoppingList.query.filter_by(list_id=id, user_id=session["user"]).first()

        if lists is not None:
            lists.delete()

            response = jsonify({"success": "Shopping list delete successful!"})
            response.status_code = 202
            return response

        else:
            response = jsonify({"error": "Shopping list with id: " + id + " not found!"})
            response.status_code = 404
            return response


@app.route("/shoppinglists/<id>/items", methods=['POST'])
@auth.login_required
def shopping_list_items(id):
    if request.method == "POST":

        try:
            int(id)
        except:
            response = jsonify({"error": "Shopping list id: " + id + " is not a valid id!"})
            response.status_code = 500
            return response

        form = ShoppingListItemForm()

        if form.validate_on_submit():

            if ShoppingList.query.filter_by(list_id=id, user_id=session["user"]).first() is None:
                response = jsonify({"error": "Shopping list id: " + id + " is not found!"})
                response.status_code = 404
                return response

            list = ShoppingListItem(form.name.data, id, form.amount.data)
            list.save()

            list = ShoppingListItem.query\
                .filter_by(name=form.name.data, list_id=id, amount=form.amount.data).first()

            response = jsonify( list.serialize )
            response.status_code = 201
            return response

        else:
            response = jsonify({"error": form.errors})
            response.status_code = 200
            return response


@app.route("/shoppinglists/<id>/items/<item_id>", methods=['PUT', 'DELETE'])
@auth.login_required
def shopping_list_item_update(id, item_id):

    try:
        int(id)
    except:
        response = jsonify({"error": "Shopping list id: " + id + " is not a valid id!"})
        response.status_code = 500
        return response

    try:
        int(item_id)
    except:
        response = jsonify({"error": "Shopping list item id: " + item_id + " is not a valid id!"})
        response.status_code = 500
        return response

    if ShoppingList.query.filter_by(list_id=id, user_id=session["user"]).first() is None:
        response = jsonify({"error": "Shopping list with id: " + id + " not found!"})
        response.status_code = 404
        return response

    if request.method == "PUT":
        form = ShoppingListItemForm()
        if form.validate_on_submit():

            lists = ShoppingListItem.query.filter_by(item_id=item_id, list_id=id).first()

            if lists is not None:
                lists.name = form.name.data
                lists.amount = form.amount.data
                db.session.commit()

                response = jsonify({"success": "Shopping list update successful!"})
                response.status_code = 200
                return response

            else:
                response = jsonify({"error": "Shopping list item with id: " + item_id + " not found!"})
                response.status_code = 404
                return response

        else:
            response = jsonify({"error": form.errors})
            response.status_code = 200
            return response

    elif request.method == "DELETE":

        lists = ShoppingListItem.query.filter_by(list_id=id, item_id=item_id).first()

        if lists is not None:
            lists.delete()

            response = jsonify({"success": "Shopping list delete successful!"})
            response.status_code = 202
            return response

        else:
            response = jsonify({"error": "Shopping list item with id: " + item_id + " not found!"})
            response.status_code = 404
            return response


@app.route('/api/token', methods=['GET'])
@auth.login_required
def get_auth_token():
    user = session["user"]
    user = User.query.filter_by(user_id=user).first()
    token = user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })


if __name__ == '__main__':
    app.run(debug=True)