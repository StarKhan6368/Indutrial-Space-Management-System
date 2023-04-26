from flask import Blueprint, redirect, render_template,url_for
from flask_login import current_user
from ISMS import db
from ISMS.models import Sensor, User, Employee, Cluster
main = Blueprint("main", __name__)

@main.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    return render_template("index.html")


@main.route("/dashboard")
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    return render_template("dashboard.html")

@main.route("/users")
def users():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    return render_template("users.html")

@main.route("/settings")
def settings():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    return render_template("settings.html")