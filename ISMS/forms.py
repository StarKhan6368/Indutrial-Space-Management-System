from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, FileField, SelectField
from wtforms.validators import Email, Length, InputRequired, EqualTo, Optional

class LoginForm(FlaskForm):
    email_id = StringField("Email Address", validators=[InputRequired(), Email(message="Invalid email address")])
    password = PasswordField("Enter Password", validators=[InputRequired(), Length(min=8)])
    submit_login = SubmitField("Log in")
    
class RegisterForm(FlaskForm):
    emp_number = StringField("Employee Number", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired(), Length(min=2, max=20)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=2, max=20)])
    gender = SelectField("Gender", choices=[("Male", "Male"), ("Female", "Female")], validators=[InputRequired()])
    date_of_birth = DateField("Date of Birth", validators=[Optional()])
    email_id = StringField("Email Address", validators=[InputRequired(), Email(message="Invalid email address"), Length(max=40)])
    password = PasswordField("Enter Password", validators=[InputRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo("password")])
    phone_number = StringField("Phone Number", validators=[Length(min=10, max=10), Optional()])
    photo = FileField("Photo", validators=[InputRequired()])
    submit_register = SubmitField("Register")