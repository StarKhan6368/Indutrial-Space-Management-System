from flask import flash
import json
from flask import Blueprint, redirect, render_template,url_for
from flask_login import current_user
from ISMS import db
from ISMS.models import Sensor, User, Employee, Cluster
from ISMS.main.forms import DateForm
main = Blueprint("main", __name__)

@main.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    print("HELLO", current_user)
    return render_template("index.html", user=current_user)


@main.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if current_user.is_authenticated:
        form = DateForm()
        if form.validate_on_submit():
            print(form.start_date.data, form.end_date.data)
        return render_template("dashboard.html", form=form, user=current_user)
    return redirect(url_for('users.login'))

@main.route("/employees")
def users():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    return render_template("employees.html", user=current_user)

@main.route("/settings")
def settings():
    return "NOPE"