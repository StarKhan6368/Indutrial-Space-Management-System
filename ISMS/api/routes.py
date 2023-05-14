from flask import abort
from ISMS import db
import json
from sqlalchemy import desc
from ISMS.api.utils import prettify_data, get_datetimes, is_host_responsive
from flask import Blueprint, redirect, url_for, request
from ISMS.models import Sensor, Employee, Cluster, User
from flask_login import current_user
api = Blueprint("api", __name__)


@api.route("/api/employees", methods=["POST"])
def employees():
    if not current_user.is_authenticated and not current_user.is_admin:
        return json.dumps({"error": 403, "message": "Unauthorized Access"})
    requested_fields = request.get_json() or []
    all_employees = Employee.query.all()
    employees_dict = [employee.as_dict(requested_fields) for employee in all_employees]
    return json.dumps(employees_dict, default=str)

@api.route("/api/user/confirm", methods=["POST"])
def confirm_user_api():
    if not current_user.is_authenticated and not current_user.is_admin:
        return json.dumps({"error": 403, "message": "Unauthorized Access"})
    employee_id = request.get_json()["emp_id"]
    user = User.query.filter_by(emp_id=employee_id).first()
    user.status = "OFFLINE"
    db.session.commit()
    return json.dumps({"message": "User Confirmed"}, default=str)

@api.route("/api/users/filter", methods=["POST"])
def filter_users():
    if not current_user.is_authenticated and not current_user.is_admin:
        return json.dumps({"error": 403, "message": "Unauthorized Access"})
    request_data = request.get_json()
    queried_users = User.query.filter_by(**request_data).all()
    users_dict = [user.as_dict([]) for user in queried_users]
    return json.dumps(users_dict, default=str)
    
@api.route("/api/employees/<emp_id>")
def get_employee(emp_id):
    if not current_user.is_authenticated and not current_user.is_admin:
        return json.dumps({"error": 403, "message": "Unauthorized Access"})
    employee = Employee.query.filter_by(emp_id=emp_id).first()
    return json.dumps(employee.as_dict([]), default=str)


@api.route("/api/clusters")
def clusters():
    if not current_user.is_authenticated:
        return json.dumps({"error": 403, "message": "Unauthorized Access"})
    all_clusters = Cluster.query.all()
    for cluster in all_clusters:
        cluster.camera_status = "ONLINE" if is_host_responsive(cluster.camera) else "OFFLINE"
    db.session.commit()
    if current_user.is_admin:
        data = {"is_admin": True, "clusters": [cluster.as_dict([]) for cluster in all_clusters]}
    else:
        data = {"is_admin": False,"clusters": [cluster.as_dict(["id","name", "location","status"]) for cluster in all_clusters]}
    return json.dumps(data, default=str)


@api.route("/api/clusters/<cluster_id>/latest")
def latest(cluster_id):
    if not current_user.is_authenticated:
        return json.dumps({"error": 403, "message": "Unauthorized Access"})
    latest_sensor = Sensor.query.filter_by(cluster_id=cluster_id).order_by(desc(Sensor.date_time)).first()
    if latest_sensor:
        return json.dumps(latest_sensor.as_dict(), default=str)
    else:
        return json.dumps([], default=str)


@api.route("/api/clusters/<cluster_id>", methods=["POST"])
def sensors(cluster_id):
    if not current_user.is_authenticated:
        return json.dumps({"error": 403, "message": "Unauthorized Access"})
    payload = request.get_json() or []
    start_datetime, end_datetime = get_datetimes(payload)
    data = Sensor.query.filter(
        Sensor.date_time >= start_datetime,
        Sensor.date_time <= end_datetime
    ).order_by(desc(Sensor.date_time))
    data = data.limit(30).all() if not payload.get('from') else data.all()
    return prettify_data(data)


@api.route("/api/thresholds")
def get_thresholds():
    return json.dumps({
        "temperature": 40, "humidity": 60, "pressure": 1000, "lpg": 400, "methane": 400,
        "smoke": 400, "hydrogen": 400, "ppm": 500, "free_heap":10240
    })
