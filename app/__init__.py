
# # import a the class that will allow us initialize a flask application
# from flask import Flask
#
# from .instance.config import app_config
# from flask_sqlalchemy import SQLAlchemy
#
# # initialize the flask application
# app = Flask(__name__)
#
# # instruct the django application to use the config file to collect settings
# app.config.from_object('config')
#
# db = SQLAlchemy(app)
#
# # when app is initialized, get our routes and functions to process requests
#from . import models
#
#
#
#
# def create_app(config_name):
#     app = Flask(__name__)
#     app.config.from_object(app_config[config_name])
#     app.config.from_pyfile('config.py')
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     db.init_app(app)
#
#     return app
