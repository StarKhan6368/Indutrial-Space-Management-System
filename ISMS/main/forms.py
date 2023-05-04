from flask_wtf import FlaskForm
from wtforms import DateTimeLocalField, SubmitField
from wtforms.validators import InputRequired

class DateForm(FlaskForm):
    start_date = DateTimeLocalField("From", format="%Y-%m-%-dT%-H:%M", validators=[InputRequired()])
    end_date = DateTimeLocalField("To", format="%Y-%m-%-dT%-H:%M", validators=[InputRequired()])
    submit_date = SubmitField("Submit")
