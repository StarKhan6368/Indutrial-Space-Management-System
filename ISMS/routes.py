from flask import render_template, redirect, url_for, flash, get_flashed_messages
from ISMS import app
from ISMS.forms import LoginForm, RegisterForm
from ISMS.database import User

@app.route("/login", methods=["GET","POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        pass
    return render_template("login.html", form=login_form)

@app.route("/")
def index():
        data = User.query.all()
        for item in data:
            print(item)
        return "Hello World"
