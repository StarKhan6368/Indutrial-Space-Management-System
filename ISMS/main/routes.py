from flask import flash, abort
import json
from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user
from ISMS import db
from ISMS.models import Sensor, User, Employee, Cluster
main = Blueprint("main", __name__)


@main.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    return render_template("index.html")


@main.route("/clusters")
def clusters():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    return render_template("clusters.html")


@main.route("/clusters/<cluster_id>")
def cluster(cluster_id):
    if current_user.is_authenticated:
        return render_template("dashboard.html")
    return redirect(url_for('users.login'))


@main.route("/employees")
def users():
    if not (current_user.is_authenticated and current_user.is_admin):
        return abort(403)
    return render_template("employees.html")

@main.route("/employees/<emp_id>")
def get_employee(emp_id):
    if not (current_user.is_authenticated and current_user.is_admin):
        return abort(403)
    return render_template("employee.html", emp_id=emp_id)

@main.route("/confirm_user")
def confirm_user():
    if not (current_user.is_authenticated and current_user.is_admin):
        return abort(403)
    return render_template("confirm_user.html")

@main.route("/settings")
def settings():
    if not (current_user.is_authenticated and current_user.is_admin):
        return abort(403)
    return "NOPEE"
