from flask import abort
from ISMS import db
import json, datetime
from sqlalchemy import desc
from ISMS.api.utils import prettify_data
from flask import Blueprint, redirect, url_for, request
from ISMS.models import Sensor, Employee, Cluster, User
from flask_login import current_user
api = Blueprint("api", __name__)


@api.route("/api/employees", methods=["POST"])
def employees():
    if not current_user.is_authenticated and not current_user.is_admin:
        return json.dumps({"Error": 403, "Message": "Unauthorized Access"})
    values = request.get_json() or []
    data = Employee.query.all()
    employee_dict = [e.as_dict(values) for e in data]
    return json.dumps(employee_dict, default=str)

@api.route("/api/user/confirm", methods=["POST"])
def confirm_user_api():
    if not current_user.is_authenticated and not current_user.is_admin:
        return json.dumps({"Error": 403, "Message": "Unauthorized Access"})
    emp_id = request.get_json()["emp_id"]
    user = User.query.filter_by(emp_id=emp_id).first()
    user.status = "OFFLINE"
    db.session.commit()
    return json.dumps({"Message": "User Confirmed"}, default=str)

@api.route("/api/employees/filter", methods=["POST"])
def get_pending():
    if not current_user.is_authenticated and not current_user.is_admin:
        return json.dumps({"Error": 403, "Message": "Unauthorized Access"})
    values = request.get_json()
    data = User.query.filter_by(**values).all()
    users_dict = [e.as_dict([]) for e in data]
    return json.dumps(users_dict, default=str)
    
@api.route("/api/employees/<emp_id>")
def get_employee(emp_id):
    if not current_user.is_authenticated and not current_user.is_admin:
        return json.dumps({"Error": 403, "Message": "Unauthorized Access"})
    data = Employee.query.filter_by(emp_id=emp_id).first()
    return json.dumps(data.as_dict([]), default=str)


@api.route("/api/clusters")
def clusters():
    if not current_user.is_authenticated:
        return json.dumps({"Error": 403, "Message": "Unauthorized Access"})
    data = Cluster.query.all()
    if current_user.is_admin:
        data = {"is_admin": True, "clusters": [c.as_dict([]) for c in data]}
    else:
        data = {"is_admin": False,"clusters": [c.as_dict(["id","name", "location","status"]) for c in data]}
    return json.dumps(data, default=str)


@api.route("/api/clusters/<cluster_id>/latest")
def latest(cluster_id):
    if not current_user.is_authenticated:
        return json.dumps({"Error": 403, "Message": "Unauthorized Access"})
    data = Sensor.query.filter_by(cluster_id=cluster_id).order_by(desc(Sensor.date_time)).first()
    return json.dumps(data.as_dict(), default=str) if data else json.dumps([], default=str)


@api.route("/api/clusters/<cluster_id>", methods=["POST"])
def sensors(cluster_id):
    if not current_user.is_authenticated:
        return json.dumps({"Error": 403, "Message": "Unauthorized Access"})
    values = request.get_json() or []
    if not values["from"] and not values['to']:
        start_datetime = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(seconds=19800)))
        end_datetime = start_datetime - datetime.timedelta(days=1)
    else:
        start_datetime = datetime.datetime.fromisoformat(values["from"])
        end_datetime = datetime.datetime.fromisoformat(values["to"])
        print(start_datetime, end_datetime)
    data = Sensor.query.filter(Sensor.date_time >= start_datetime).filter(Sensor.date_time <= end_datetime ).order_by(desc(Sensor.date_time))
    data = data.limit(30).all() if not values['from'] else data.all()
    print(data)
    return prettify_data(data)


@api.route("/api/thresholds")
def threshold():
    return json.dumps({
        "temperature": 40, "humidity": 60, "pressure": 1000, "lpg": 400, "methane": 400,
        "smoke": 400, "hydrogen": 400, "ppm": 500, "free_heap":10240
    })
