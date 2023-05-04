import json
from flask import Blueprint, redirect, render_template,url_for, request
from ISMS.models import Sensor, Employee
from flask_login import current_user
api = Blueprint("api", __name__)

@api.route("/api/latest")
def latest():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    data = Sensor.query.filter_by(cluster_id=1).first()
    return json.dumps(data.as_dict(), default=str)

@api.route("/api/employees", methods=["POST"])
def employees():
        if not current_user.is_authenticated:
            return redirect(url_for('users.login'))
        values = request.get_json() or []
        data = Employee.query.all()
        employee_dict = [e.as_dict(values) for e in data]
        return json.dumps(employee_dict, default=str)

@api.route("/api/employees/<emp_id>")
def get_employee(emp_id):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    data = Employee.query.filter_by(emp_id=emp_id).first()
    return json.dumps(data.as_dict([]), default=str)

@api.route("/api/thresholds")
def threshold():
    return json.dumps({
        "temperature": 40, "humidity": 40, "pressure": 40, "lpg": 40, "methane": 40,
        "smoke": 40, "hydrogen": 40, "ppm": 40
    })