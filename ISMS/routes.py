from flask import render_template, redirect, url_for, flash, get_flashed_messages
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, current_user
from ISMS import app, db
from sqlalchemy import text
from ISMS.forms import LoginForm, RegisterForm
from ISMS.models import User

@app.route("/login", methods=["GET","POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email_id.data).first()
        if user and login_form.password.data == user.password:
            login_user(user, remember=login_form.remember_me.data)
            return redirect(url_for('index'))
        else:
            flash("Invalid email or password", "danger")
    return render_template("login.html", form=login_form)

@app.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template("index.html")

@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('login'))
