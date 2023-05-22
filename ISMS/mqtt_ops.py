import json, datetime
from pathlib import Path
from ISMS.api.utils import is_host_responsive
from ISMS import app, db, mqtt
from ISMS.models import Cluster, Sensor, Employee, Entry
from ISMS.face_recog import Camera

with app.app_context():
    all_clusters = Cluster.query.all()
    for cluster in all_clusters:
        cluster.camera_status = "ONLINE" if is_host_responsive(cluster.camera) else "OFFLINE"
    db.session.commit()
print("All Cluster Conditions Have Been Updated, Starting ISMS Flask App...")
        
def message_handler(data):
    if data["topic"] == "RFID_DATA":
        cam_data_handler(json.loads(data["payload"]))
    elif data["topic"] == "ENV_DATA":
        env_data_handler(json.loads(data["payload"]))
    else:
        print(data)
        
def env_data_handler(data):
    if data.get("temperature"):
        with app.app_context():
            cluster = Cluster.query.filter_by(id=data["cluster_id"]).first()
            cluster.status = "ONLINE"
            readings = Sensor(date_time=data["date_time"], cluster_id = data["cluster_id"], temperature=float(data["temperature"]), humidity=float(data["humidity"]),
                            pressure=float(data["pressure"]), lpg=data["lpg"], methane=data["methane"],smoke=data["smoke"],
                            hydrogen=data["hydrogen"],ppm=data["ppm"], free_heap=data["free_heap"])
            db.session.add(readings)
            db.session.commit()
    elif data.get("status"):
        with app.app_context():
            cluster = Cluster.query.filter_by(id=data["cluster_id"]).first()
            cluster.status = data["status"]
            db.session.commit()
            
def cam_data_handler(data):
    if data.get("rfid"):
        with app.app_context():
            cluster = Cluster.query.filter_by(id=data["cluster_id"]).first()
            cluster.camera_status = "ONLINE" if is_host_responsive(cluster.camera) else "OFFLINE"
            db.session.commit()
            if cluster.camera_status == "ONLINE":
                camera = Camera(f"http://{cluster.camera}")
                employee = Employee.query.filter_by(emp_id = data["rfid"]).first()
                if  not employee:
                    message = json.dumps({"rfid":data["rfid"], "result":" INVALID RFID", "date_time":datetime.datetime.now()}, default=str)
                    print("FACE ID Response: ", message)
                    mqtt.publish("FACE_DATA", message)
                    return None
                recognized, filename = camera.recognize(employee.enc_photo, intensity=50)
                result = f" ACCESS {'GRANTED' if recognized else 'DENIED '}  PLEASE PROCEED "
                message = json.dumps({"rfid":data["rfid"], "result":result, "date_time":datetime.datetime.now()}, default=str)
                print("FACE ID Response: ", message)
                mqtt.publish("FACE_DATA", message)
                if recognized:
                    new_entry = Entry(date_time=datetime.datetime.now(), cluster_id=data["cluster_id"], emp_id=data["rfid"], photo=filename)
                    db.session.add(new_entry)
                    db.session.commit()
                else:
                    Path.unlink(filename)
            else:
                message = json.dumps({"rfid":data["rfid"], "result":" CAMERA OFFLINE ", "date_time":datetime.datetime.now()}, default=str)
                print("FACE ID Response: ", message)
                mqtt.publish("FACE_DATA", message)
        