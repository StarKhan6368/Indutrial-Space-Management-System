# Import Needed Libraries
from micropython import const
from servo import Servo
import bme280, ntptime, json, network, gc, machine, time
from mfrc522 import MFRC522
from i2c_lcd import I2cLcd
from MQ2 import MQ2
from buzzer import BuzzerPlayer
from MQ135 import MQ135
from umqttsimple import MQTTClient

# Collect Garbage and enable Automatic Garbage Collection
gc.collect()
gc.enable()

# CONSTANT VALUES WILL BE USED LATER IN THE SCRIPT
LCD_I2C_ADDR = const(0x27)
LCD_TOTAL_ROWS = const(2)
LCD_TOTAL_COLUMNS = const(16)
WIFI_SSID = const("<user_name>")
WIFI_PASSWORD = const("<wifi_password>")
MQTT_SERVER = const("192.168.0.111")
TCP_PORT = const(1883)
CLIENT_ID = const("ESP-32")
MQTT_USER = const("<mqtt_username>")
MQTT_PASSWORD = const("<mqtt_password>")
ENV_TOPIC = const("ENV_DATA")
RFID_TOPIC = const("RFID_DATA")
FACE_TOPIC = const("FACE_DATA")
MUSIC_TOPIC = const("MUSIC_DATA")
RELAY_TOPIC = const("RELAY_DATA")
CLUSTER_ID = const(1)

# VALUES WILL BE MODIFIED LATER IN THE SCRIPT
rfid_detected = False
face_recon_topic = ""
face_recon_message = ""
face_response = False
recon_init = False
granted = False

# Initiating Sensors and LCD Display
buzz = BuzzerPlayer(26)
my_servo = Servo(pin_id=25)
ir1 = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_DOWN)
ir2 = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
relay = machine.Pin(13, machine.Pin.OUT)
relay.value(1)
i2c = machine.I2C(1, scl=machine.Pin(22), sda=machine.Pin(21), freq=10000)
lcd = I2cLcd(i2c, LCD_I2C_ADDR, LCD_TOTAL_ROWS, LCD_TOTAL_COLUMNS)
bme = bme280.BME280(i2c=i2c)
mq2 = MQ2(pinData = machine.Pin(35))
mq135 = MQ135(machine.Pin(34))
spi = machine.SPI(2, baudrate=2500000, polarity=0, phase=0)
spi.init()
rdr = MFRC522(spi=spi, gpioRst=4, gpioCs=5)
    
# WiFi Connection Block
def connect_to_wifi(SSID, PASSWORD):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    if station.isconnected() == False:
        print(f"WiFi Not connected, Connecting to: {SSID}")
        lcd.putstr(f"  CONN TO WIFI   SSID:{SSID.upper()}")
        station.connect(SSID, PASSWORD)
    else:
        print(f"Wifi Already Connected to: {SSID}")
        lcd.putstr(f" WIFI CONN DONE  SSID:{SSID.upper()} ")
        time.sleep(0.5)
    while not station.isconnected():
        lcd.move_to(0,1)
        lcd.putstr("CONN PENDING....")
    print("Printing IP Config...")
    print(station.ifconfig())
connect_to_wifi(WIFI_SSID, WIFI_PASSWORD)

# Synchronize System time via Internet and ntptime module
print("Synchronizing system time with ntptime")
ntptime.settime()

# MQTT Connection Functions
def connect(show_on_lcd = True):
    lcd.clear()
    print(f"Connecting to MQTT Server: {MQTT_SERVER} with Client Id: {CLIENT_ID}")
    if show_on_lcd:
        lcd.putstr(f"  CONN TO MQTT    {MQTT_SERVER.upper()} ")
        time.sleep(0.5)
    client = MQTTClient(CLIENT_ID, MQTT_SERVER, 1883, MQTT_USER, MQTT_PASSWORD, keepalive=30, ssl=False, ssl_params={})
    client.set_last_will(ENV_TOPIC, json.dumps({"status":"OFFLINE", "cluster_id":CLUSTER_ID}))
    client.connect()
    return client

# Function to reconnect to MQTT Server upon Failure
def reconnect():
    global client
    print("Connection to MQTT Failed, Retrying Again after 5 Seconds")
    lcd.clear()
    lcd.putstr("MQTT CONN FAILEDMQTT RECONN INIT")
    time.sleep(5)
    # Try Connecting to MQTT Again
    try:
        client = connect()
    # Hard Reset ESP-32 If MQTT Connection Fails Again
    except:
        lcd.clear()
        print("Connection Failed Machine will now reset")
        lcd.putstr("MQTT CONN FAILEDMACHINE RESET...")
        time.sleep(2)
        machine.reset()
    
# MQ-2 Gas Sensor Calibration
lcd.clear()
print("Calibrating MQ2 Sensor")
lcd.putstr(" CALIBRATING MQ  GAS SENSORS...  ")
mq2.calibrate()
lcd.clear()
print("MQ2 Sensor Calibrations Complete")
lcd.putstr("  CALIBRATIONS      COMPLETE    ")


# Initiate MQTT Connection
try:
    client = connect()
# If MQTT Connection Fails
except OSError as e:
    reconnect()
finally:
    lcd.clear()
    print("Sucessfully Connected to MQTT Server")
    lcd.putstr(f" MQTT CONN DONE CLIENT ID:{CLIENT_ID}")
    time.sleep(0.5)
