from flask import flash, abort, request
import json
from pathlib import Path
from flask import Blueprint, redirect, render_template, url_for, send_file
from flask_login import current_user
from ISMS import db
from ISMS.main.forms import EmployeeForm
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
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    return render_template("dashboard.html")


@main.route("/employees")
def users():
    if not (current_user.is_authenticated and current_user.is_admin):
        return abort(403)
    return render_template("employees.html")

@main.route("/employees/<emp_id>")
def get_employee(emp_id):
    if not (current_user.is_authenticated and current_user.is_admin):
        if current_user.is_authenticated and current_user.emp_id == emp_id:
            return render_template("employee.html", emp_id=emp_id)
        else:
            return abort(403)
    return render_template("employee.html", emp_id=emp_id)

@main.route("/confirm_user")
def confirm_user():
    if not (current_user.is_authenticated and current_user.is_admin):
        return abort(403)
    return render_template("confirm_user.html")

@main.route("/settings")
def settings():
    return abort(404)

@main.route("/add_employee", methods=["GET","POST"])
def add_employee():
    if not (current_user.is_authenticated and current_user.is_admin):
        return abort(403)
    employee_from = EmployeeForm()
    if employee_from.validate_on_submit():
        new_emp = Employee(emp_id=employee_from.emp_id.data,first_name=employee_from.first_name.data,last_name=employee_from.last_name.data,
                           gender=employee_from.gender.data, date_of_birth=employee_from.date_of_birth.data,phone_number=employee_from.phone_number.data,
                           address=employee_from.address.data, position=employee_from.position.data, enc_photo=employee_from.face_enc.data)
        db.session.add(new_emp)
        db.session.commit()
    elif request.method == "POST":
        flash("Invalid Form")
    return render_template("add_employee.html", form = employee_from)

@main.route("/entry/<filename>")
def return_image(filename):
    return send_file(f"/home/starkhan/Major Project/face_recon/{filename}", mimetype="image/jpg")

@main.route("/rtttl")
def rtttl():
    if not (current_user.is_authenticated and current_user.is_admin):
        return abort(403)
    return render_template("play_rtttl.html")