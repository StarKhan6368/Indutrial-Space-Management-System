import json, datetime
from sqlalchemy import desc
from ISMS.api.utils import prettify_data
from flask import Blueprint, redirect, render_template, url_for, request
from ISMS.models import Sensor, Employee, Cluster
from flask_login import current_user
api = Blueprint("api", __name__)


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


@api.route("/api/clusters")
def clusters():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    data = Cluster.query.all()
    data = [cluster.as_dict([]) for cluster in data]
    return json.dumps(data, default=str)


@api.route("/api/clusters/<cluster_id>/latest")
def latest(cluster_id):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    data = Sensor.query.filter_by(cluster_id=cluster_id).order_by(desc(Sensor.date_time)).first()
    return json.dumps(data.as_dict(), default=str)


@api.route("/api/clusters/<cluster_id>", methods=["POST"])
def sensors(cluster_id):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    values = request.get_json() or []
    if not values["from"] and not values['to']:
        start_datetime = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(seconds=19800)))
        end_datetime = start_datetime - datetime.timedelta(days=1)
    else:
        start_datetime = datetime.datetime.fromisoformat(values["from"])
        end_datetime = datetime.datetime.fromisoformat(values["to"])
    data = Sensor.query.filter(Sensor.date_time <= start_datetime).filter(Sensor.date_time >= end_datetime ).order_by(desc(Sensor.date_time))
    data = data.limit(30).all() if not values['from'] else data.all()
    return prettify_data(data)


@api.route("/api/thresholds")
def threshold():
    return json.dumps({
        "temperature": 40, "humidity": 60, "pressure": 1000, "lpg": 400, "methane": 400,
        "smoke": 400, "hydrogen": 400, "ppm": 500, "free_heap":10240
    })
