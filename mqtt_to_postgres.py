from ISMS.models import Sensor
from paho.mqtt import client as mqtt_client
from ISMS import app
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
            print(data)
        else:
            print(payload)

    client.subscribe(TOPIC)
    client.on_message = on_message

def process_me():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
