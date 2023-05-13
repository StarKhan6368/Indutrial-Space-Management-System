from ISMS.models import Sensor, Cluster, Employee
from paho.mqtt import client as mqtt_client
from ISMS import app, db
from camera import Camera
import json, datetime

BROKER = '192.168.0.111'
CAM_API = "http://192.168.0.123"
PORT = 1883
ESP_ENV_TOPIC = "ENV_DATA"
ESP_CAM_TOPIC = "RFID_DATA"
FACE_RECON_TOPIC = "FACE_DATA"
USERNAME = "<mqtt_username>"
PASSWORD = "<mqtt_password>"
CLIENT_ID = "Flask-App"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(CLIENT_ID)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    return client

def env_subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        if "temperature" in data:
            with app.app_context():
                cluster = Cluster.query.filter_by(id=data["cluster_id"]).first()
                cluster.status = "ONLINE"
                readings = Sensor(date_time=data["date_time"], cluster_id = data["cluster_id"], temperature=float(data["temperature"][:-1]), humidity=float(data["humidity"][:-1]),
                              pressure=float(data["pressure"][:-3]), lpg=data["lpg"], methane=data["methane"],smoke=data["smoke"],
                              hydrogen=data["hydrogen"],ppm=data["ppm"], free_heap=data["free_heap"])
                db.session.add(readings)
                db.session.commit()
        elif "status" in data:
            with app.app_context():
                cluster = Cluster.query.filter_by(id=data["cluster_id"]).first()
                cluster.status = data["status"]
                db.session.commit()
    client.subscribe(ESP_ENV_TOPIC)
    client.on_message = on_message
    

def cam_subscribe(client: mqtt_client):
    camera = Camera(CAM_API)
    def on_message(client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        print(data, end="\n<------------->\n")
        if "rfid_detected" in data:
            with app.app_context():
                employee = Employee.query.filter_by(emp_id = data["rfid"]).first()
            result = "GRANTED" if camera.recognize(employee.enc_photo, intensity=50) else "DENIED "
            client.publish(FACE_RECON_TOPIC,json.dumps({"Access":result, "date_time":datetime.datetime.now()}, default=str))
    client.subscribe(ESP_CAM_TOPIC)
    client.on_message = on_message

def mqtt_start():
    print("Connecting to MQTT Server")
    client = connect_mqtt()
    env_subscribe(client)
    # cam_subscribe(client)
    client.loop_forever()
    
if __name__ == "__main__":
    mqtt_start()
