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

models.db.init_app(app)
mail = Mail(app)

from . import v1_views,v2_views