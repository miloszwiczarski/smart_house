from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, URL, Length, Email


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()], render_kw={"placeholder": "admin"})
    password = PasswordField("Password", validators=[DataRequired(), Length(min=5)], render_kw={"placeholder": "haslo"})
    confirm_password = PasswordField("confirm password", validators=[DataRequired(), Length(min=5)], render_kw={"placeholder": "haslo"})
    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()], render_kw={"placeholder": "admin"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "haslo"})
    submit = SubmitField("Log in")
