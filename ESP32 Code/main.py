# Import Required Libraries
import uasyncio as asyncio

# Function to reconnect to MQTT if connection drops
def reconnect_to_mqtt():
    global recon_init
    try:
        print("OS Error Has Occurred Re-Establishing Connection with MQTT Server")
        recon_init = True
        time.sleep(2)
        client = connect(show_on_lcd=False)
    except OSError:
        print("Connection Failed Machine will now reset")
        time.sleep(5)
        machine.reset()
        
# Asynchronous Function to measure sensor reading and send to the MQTT Server on specified topic
# Ideally every 5 Seconds, although it may vary MQ135 Not Implemented Yet
async def measure_and_send():
    global temperature, humidity, pressure, smoke, hydrogen, methane, lpg, ppm
    while True:
        temperature = bme.temperature
        humidity = bme.humidity
        pressure = bme.pressure
        await asyncio.sleep(0)
        smoke = mq2.readSmoke()
        hydrogen = mq2.readHydrogen()
        methane = mq2.readMethane()
        lpg = mq2.readLPG()
        await asyncio.sleep(0)
        ppm = mq135.get_corrected_ppm(temperature, humidity)
        await asyncio.sleep(0)
        message = {"date_time": time.localtime(time.time() + 19800), "free_heap": gc.mem_free(), "cluster_id":CLUSTER_ID, "temperature":temperature, "humidity":humidity, "pressure":pressure, "smoke":smoke, "hydrogen":hydrogen, "methane":methane, "lpg":lpg, "ppm": ppm}
        try:
            client.publish(ENV_TOPIC, json.dumps(message), qos=0)
            await asyncio.sleep(0)
        except OSError:
            if not recon_init:
                reconnect_to_mqtt()
        print(f"Published ENV Message to MQTT Server on: {message['date_time']}")
        await asyncio.sleep(4)
        
# Asynchronous Function to display Sensor readings onto LCD
async def display_readings():
    lcd.clear()
    lcd.putstr(f"T:{temperature:.2f}  H:{humidity:.2f}PRESSURE: {pressure:.2f}")
    await asyncio.sleep(1)
    mq2_safe = lpg < 500  or methane < 500 or hydrogen < 500 or smoke < 500
    bme_safe = temperature < 35 or humidity < 60 or pressure < 1000
    update_relay(mq2_safe and bme_safe)
    lcd.clear()
    lcd.putstr(f"MQ2: VALS {'SAFE  ' if mq2_safe else 'UNSAFE'}MQ135:{ppm:.2f} PPM")
    await asyncio.sleep(1)
    
async def update_relay(values):
    if not values:
        realy.value(0)
    else:
        relay.value(1)
        
# Asyncronous Function for controlling LCD Display Output
async def display():
    global rfid_detected, face_response
    while True:
        if rfid_detected:
            lcd.clear()
            lcd.putstr(f" RFID DATA READ ID: HEX {card_id}")
            lcd.putstr(" AWAIT RESPONSE ")
            await asyncio.sleep(0.5)
            rfid_detected = False
            if face_response:
                lcd.putstr(face_recon_message)
                if granted:
                    await watchmen()
                else:
                    await asyncio.sleep(1)
                face_response = False
            else:
                lcd.putstr(" FACE RECON SVR ERR TIMEOUT RETRY")
        else:
            await display_readings()
            
async def watchmen():
    global granted
    print("Servo Unlocked")
    while ir1.value():
        await asyncio.sleep(0)
    buzz.tone(1000, 200, 256)
    while ir2.value():
        await asyncio.sleep(0)
    buzz.tone(1000, 200, 256)
    print("Servo Locked")
    granted = False

# Asyncronous Function to keep reading from MFRC-522 until card is detected
async def rfid_and_face_recon():
    global rfid_detected, card_id
    while True:
        (stat, _) = rdr.request(rdr.REQIDL)
        if stat == rdr.OK and rfid_detected == False:
            (stat, raw_uid) = rdr.anticoll()
            try:
                card_id = "%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
            except IndexError:
                continue
            buzz.tone(2000, 200, 256)
            time.sleep(0.1)
            buzz.tone(2000, 200, 256)
            print("<!----------------!>")
            print("RFID Card Detected with ID:", card_id)
            message = {"rfid_detected": True, "rfid": card_id, "date_time": time.localtime(time.time() + 19800), "cluster_id": CLUSTER_ID}
            try:
                client.publish(RFID_TOPIC, json.dumps(message), qos=0)
            except OSError:
                if not recon_init:
                    reconnect_to_mqtt()
            print(f"Published RFID Message to MQTT Server on: {message['date_time']}")
            print("<!----------------!>")
            rfid_detected = True
            await asyncio.sleep(1)
            client.check_msg()
            await asyncio.sleep(5)
        try:
            client.check_msg()
        except OSError:
            if not recon_init:
                reconnect_to_mqtt()
        await asyncio.sleep(0)

def mqtt_callback(topic, message):
    global face_recon_topic, face_recon_message, face_response, granted
    message = json.loads(message)
    topic = topic.decode('utf-8')
    if topic == FACE_TOPIC:
        print("<!----------------!>")
        print(f"Recieved FACE_RECON Message from MQTT Server on: {message['date_time']}")
        print("<!----------------!>")
        face_recon_message = message.get("result")
        if "GRANTED" in face_recon_message:
            granted = True
        else:
            granted = False
        face_response = True if face_recon_message else False
    elif topic == RELAY_TOPIC:
        if "value" in message:
            relay.value(message["value"])
    elif topic == MUSIC_TOPIC:
        if "melody" in message:
            buzz.play_rtttl(message["melody"])
    
# Collect Garbage
gc.collect()

# Subscribe to FACE_RECON topic
client.set_callback(mqtt_callback)
client.subscribe(FACE_TOPIC, qos=0)
client.subscribe(MUSIC_TOPIC, qos=0)
client.subscribe(RELAY_TOPIC, qos=0)

async def main():
    measure_task = asyncio.create_task(measure_and_send())
    display_task = asyncio.create_task(display())
    rfid_task = asyncio.create_task(rfid_and_face_recon())
    await measure_task
    await display_task
    await rfid_task
    
asyncio.run(main())