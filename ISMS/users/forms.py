from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Email, Length, InputRequired, EqualTo

class LoginForm(FlaskForm):
    email_id = StringField("Email Address", validators=[InputRequired(), Email(message="Invalid email address")])
    password = PasswordField("Enter Password", validators=[InputRequired(), Length(min=8)])
    remember_me = BooleanField("Remember Me")
    submit_login = SubmitField("Log in")
    
class SignupForm(FlaskForm):
    email_id = StringField("Email Address", validators=[InputRequired(), Email(message="Invalid email address")])
    emp_id = StringField("Enter Employee ID", validators=[InputRequired(), Length(min=8, max=8)])
    password = PasswordField("Enter Password", validators=[InputRequired(), Length(min=8), 
                EqualTo("confirm_password", message="Passwords must match")])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), Length(min=8)])
    submit_signup = SubmitField("Sign up")

    