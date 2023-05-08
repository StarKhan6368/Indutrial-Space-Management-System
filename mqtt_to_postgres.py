from ISMS.models import Sensor, Cluster
from paho.mqtt import client as mqtt_client
from ISMS import app, db
import json

BROKER = '192.168.0.123'
PORT = 1883
TOPIC = "esp32"
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

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        print(data)
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
            
            

    client.subscribe(TOPIC)
    client.on_message = on_message

def mqtt_start():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
    
mqtt_start()
