import json, datetime
from ISMS import app, db, mqtt
from ISMS.models import Cluster, Sensor, Employee
from ISMS.face_recog import Camera

def message_handler(data):
    if data["topic"] == "RFID_DATA":
        cam_data_handler(json.loads(data["payload"]))
    elif data["topic"] == "ENV_DATA":
        env_data_handler(json.loads(data["payload"]))
    else:
        print(data)
        
def env_data_handler(data):
    if data["temperature"]:
        with app.app_context():
            cluster = Cluster.query.filter_by(id=data["cluster_id"]).first()
            cluster.status = "ONLINE"
            readings = Sensor(date_time=data["date_time"], cluster_id = data["cluster_id"], temperature=float(data["temperature"][:-1]), humidity=float(data["humidity"][:-1]),
                            pressure=float(data["pressure"][:-3]), lpg=data["lpg"], methane=data["methane"],smoke=data["smoke"],
                            hydrogen=data["hydrogen"],ppm=data["ppm"], free_heap=data["free_heap"])
            db.session.add(readings)
            db.session.commit()
    elif data["status"]:
        with app.app_context():
            cluster = Cluster.query.filter_by(id=data["cluster_id"]).first()
            cluster.status = data["status"]
            db.session.commit()
            
def cam_data_handler(data):
    camera = Camera("http://192.168.0.123")
    if data["rfid_detected"]:
        with app.app_context():
            employee = Employee.query.filter_by(emp_id = data["rfid"]).first()
            result = "GRANTED" if camera.recognize(employee.enc_photo, intensity=50) else "DENIED "
            message = json.dumps({"rfid":data["rfid"], "Access":result, "date_time":datetime.datetime.now()}, default=str)
            print("FACE ID Response: ", message)
            mqtt.publish("FACE_DATA", message)