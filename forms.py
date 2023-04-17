from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Email, Length, InputRequired

class LoginForm(FlaskForm):
    email_id = StringField("Email Address", validators=[InputRequired(), Email(message="Invalid email address")])
    password = PasswordField("Enter Password", validators=[InputRequired(), Length(min=8)])
    remember = BooleanField("Remember Me")
    submit_login = SubmitField("Log in")
    