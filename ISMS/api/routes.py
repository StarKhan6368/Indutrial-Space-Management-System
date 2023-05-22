from flask import abort
from pathlib import Path
from ISMS import db, mqtt
import json, datetime, string, random
from ISMS.face_recog import Camera
from sqlalchemy import desc
from ISMS.api.utils import prettify_data, is_host_responsive
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
    if queried_users:
        users_dict = [user.as_dict([]) for user in queried_users]
    else:
        users_dict = {}
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

@api.route("/api/clusters_camera/<cluster_id>")
def clusters_camera(cluster_id):
    if not current_user.is_authenticated:
        return json.dumps({"error": 403, "message": "Unauthorized Access"})
    cluster = Cluster.query.filter_by(id=cluster_id).first()
    if cluster:
        return json.dumps({"camera_ip": cluster.camera, "camera_status": cluster.camera_status})
    else:
        return json.dumps({"camera_ip": "", "camera_status": ""})


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
    if payload.get("from") and not payload.get("to"):
        start_datetime = datetime.datetime.fromisoformat(payload.get("from"))
        end_datetime = datetime.datetime.fromisoformat(payload.get("to"))
    else:
        end_datetime = datetime.datetime.now()
        start_datetime = end_datetime - datetime.timedelta(minutes=30)
    data = Sensor.query.filter(
        Sensor.date_time >= start_datetime,
        Sensor.date_time <= end_datetime,
        Sensor.cluster_id == cluster_id
    ).order_by(desc(Sensor.date_time))
    return prettify_data(data.all() if payload.get("from") else data.limit(30).all())

@api.route("/api/rtttl_files")
def send_rtttl_list():
    rtttl_dir = Path("ISMS/rtttl_files")
    rtttl_file_list = [file.name for file in rtttl_dir.glob("*")]
    return json.dumps({"total": len(rtttl_file_list), "file_list": rtttl_file_list}, default=str)

@api.route("/api/mqtt_rtttl", methods=["POST"])
def publish_to_mqtt():
    if not current_user.is_authenticated and not current_user.is_admin:
        return json.dumps({"error": 403, "message": "Unauthorized Access"})
    payload = request.get_json()
    with open(f"ISMS/rtttl_files/{payload['file_name']}.txt", "r") as file:
        data = file.read()
    mqtt.publish("MUSIC_DATA", json.dumps({"melody": data.strip()}) , qos=0)
    return json.dumps({"message": "Published"}, default=str)
    
@api.route("/api/capture_and_validate", methods=["POST"])
def cap_and_validate():
    if not current_user.is_authenticated and not current_user.is_admin:
        return json.dumps({"error": 403, "message": "Unauthorized Access"})
    camera_ip = request.get_json().get("camera_ip")
    print(camera_ip)
    if camera_ip and is_host_responsive(camera_ip):
        camera = Camera(f"http://{camera_ip}")
        filename = camera.capture(filename=''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10)))
        face_encodings = camera.find_and_encode(filename)
        Path.unlink(filename)
        return json.dumps({"encoding": face_encodings}, default=str)
    else:
        return json.dumps({"encoding":[]}, default=str)
        
    
@api.route("/api/thresholds")
def get_thresholds():
    return json.dumps({
        "temperature": 40, "humidity": 60, "pressure": 1000, "lpg": 400, "methane": 400,
        "smoke": 400, "hydrogen": 400, "ppm": 500, "free_heap":10240
    })
