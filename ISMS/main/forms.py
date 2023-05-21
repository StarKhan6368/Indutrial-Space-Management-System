from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import Length, InputRequired, Optional

class EmployeeForm(FlaskForm):
    emp_id = StringField("Enter Employee ID", validators=[InputRequired(), Length(min=8, max=8)])
    first_name = StringField("Enter First Name", validators=[InputRequired(), Length(max=20)])
    last_name = StringField("Enter Last Name", validators=[InputRequired(), Length(max=20)])
    gender = SelectField("Gender", choices=["Male", "Female"])
    date_of_birth = DateField("Date of Birth", format="%Y-%m-%d", validators=[InputRequired()])
    position = SelectField("Position", choices=["Manager", "Supervisior", "Tech", "Worker", "Other"])
    phone_number= StringField("Enter Phone Number", validators=[Optional(), Length(max=10)])
    address = StringField("Enter Address", validators=[Optional()])
    face_enc = StringField("Enter Face Encoding", validators=[InputRequired(message="Make sure you capture a image first")])
    submit = SubmitField("Add Employee")