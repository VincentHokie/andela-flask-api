__author__ = 'MacUser'

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class SignUpForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('password2', validators=[DataRequired()])


class ShoppingListForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])


class ShoppingListItemForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    amount = IntegerField('name', validators=[DataRequired()])