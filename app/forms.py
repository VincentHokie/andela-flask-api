__author__ = 'MacUser'

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class SignUpForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('password2', validators=[DataRequired()])


class ShoppingListForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])


class ShoppingListItemForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    amount = IntegerField('name', validators=[DataRequired()])

class EmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])#

class PasswordResetForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired(), EqualTo('password_confirm')])
    password_confirm = PasswordField('password_confirm', validators=[DataRequired(), EqualTo('password')])