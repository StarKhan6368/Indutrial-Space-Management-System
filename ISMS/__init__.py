from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mqtt import Mqtt

app = Flask(__name__)
# Databse Configs
app.config["SECRET_KEY"] = "<SECRET_KEY>"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://<username>:<password>@localhost:5432/ISMS"
# MQTT Configs
app.config['MQTT_BROKER_URL'] = '192.168.0.111'
app.config["MQTT_CLIENT_ID"] = "ISMS"
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = '<mqtt_username>'
app.config['MQTT_PASSWORD'] = '<mqtt_password>'
app.config['MQTT_KEEPALIVE'] = 10
app.config['MQTT_TLS_ENABLED'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
mqtt = Mqtt(app)

@app.errorhandler(403)
def unauthorized(e):
    return render_template("403.html"), 403

@app.errorhandler(404)
def unauthorized(e):
    return render_template("404.html"), 40

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker..., Subscribing to required topics...")
    mqtt.subscribe('RFID_DATA')
    mqtt.subscribe('ENV_DATA')
    print("Subscriptions Complete, Checking All Cluster Conditions...")

from ISMS.mqtt_ops import message_handler
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    message_handler(data)

from ISMS.users.routes import users
from ISMS.main.routes import main
from ISMS.api.routes import api

app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(api)