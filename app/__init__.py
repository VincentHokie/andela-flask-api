import os
from . import models
from flask import Flask
from flask_mail import Mail
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["DEBUG"] = True
app.config["CSRF_ENABLED"] = True

app.config["SQLALCHEMY_DATABASE_URI"] = \
        os.environ['HEROKU_POSTGRESQL_CRIMSON_URL']

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# make wft extension consider cross-site request forgery
app.config["WTF_CSRF_ENABLED"] = False

# required when the above config is enabled, this will be used to
# generate a scrf token..should be a string that cant be easily
# guessed in production
app.config["SECRET_KEY"] = os.environ['SECRET_KEY']

# email server
app.config["MAIL_SERVER"] = os.environ['MAIL_SERVER']
app.config["MAIL_PORT"] = os.environ['MAIL_PORT']
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.environ['MAIL_USERNAME']
app.config["MAIL_PASSWORD"] = os.environ['MAIL_PASSWORD']
app.config["MAIL_DEFAULT_SENDER"] = os.environ['MAIL_DEFAULT_SENDER']

# administrator list
ADMINS = ['your-gmail-username@gmail.com']

models.db.init_app(app)
mail = Mail(app)

from . import v1_views, v2_views
