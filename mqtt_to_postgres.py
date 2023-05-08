from ISMS.models import Sensor
from paho.mqtt import client as mqtt_client
from ISMS import app, db
import json

BROKER = 'broker.emqx.io'
PORT = 1883
TOPIC = "test"
USERNAME = "emqx"
PASSWORD = "public"
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
        if "temp" in payload:
            data = json.loads(payload)
            with app.app_context():
                readings = Sensor(date_time=data["date_time"], cluster_id = data["cluster_id"], temperature=float(data["temperature"][:-1]), humidity=float(data["humidity"][:-1]),
                              pressure=float(data["pressure"][:-3]), lpg=data["lpg"], methane=data["methane"],smoke=data["smoke"],
                              hydrogen=data["hydrogen"],ppm=data["ppm"], free_heap=data["free_heap"])
                db.session.add(readings)
                db.session.commit()
        else:
            print(payload)

    client.subscribe(TOPIC)
    client.on_message = on_message

def process_me():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
    
process_me()
