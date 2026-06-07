import paho.mqtt.client as mqtt #just building up connections
import datetime as dt
from database import *
import time
import pickle
import json
from shutdown import *
import logging
from logging.handlers import RotatingFileHandler
import os
import threading
from flask import Flask, request, jsonify

LOGDIR = '/var/log/weather_station' # logging added in version 139
os.makedirs(LOGDIR, exist_ok=True)
SHUTDOWN_TOPIC = 'weather_station/mydevice/control'

app = Flask(__name__)#version 140
connections_logger = logging.getLogger("connections")
# --- Korjattu formatteri, joka lisää component-kentän automaattisesti ---
class ComponentFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, "component"):
            record.component = record.name  # fallback, estää KeyErrorin
        return super().format(record)

def make_logger(name, path, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = RotatingFileHandler(path, maxBytes=5*1024*1024, backupCount=5)

        fmt = '%(asctime)s %(levelname)s %(name)s %(component)s: %(message)s'
        formatter = ComponentFormatter(fmt)

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

# luodaan logger, käytä pienaakkosia tiedostonimissä
connections_logger = make_logger(
    'weather.sensor',
    os.path.join(LOGDIR, 'sensor.log'),
    level=logging.INFO
)

connections_logger.info('Sensor started', extra={'component': 'sensor'})

# turvallinen pickle-esimerkki (absoluuttinen polku)
#os.makedirs(os.path.dirname(PICKLE_PATH), exist_ok=True)
save_values_to_database = time.time()
timestartup = dt.datetime.now()
timestartup = timestartup.strftime("%y-%m-%d %H:%M:%S")
esp_json_message = {"kitchen_indoor_temp": 0.0, "kitchen_indoor_humidity": 0.0, "kitchen_outdoor_temp":0.0,"kitchen_outdoor_humidity":0.0,"kitchen_timestamp":timestartup,
                    "livingroom_indoor_temp":0.0, "livingroom_indoor_temp": 0.0, "livingroom_outside_temp":0.0, "livingroom_outside_humidity":0.0,
                    "livingroom_timestamp":timestartup,
                    "bedroom_temp":0.0, "bedroom_humidity": 0.0, "bedroom_timestamp": timestartup, "lux_value_kitchen":1.0, "lux_value_livingroom":1.0}

# this program is only for mqtt devices. this will send every 15 seconds pickle message to weatherstation and every 1 hour upload data to database
# here is tree esp32 wroom microcontrollers. device 1 and 2 has 2 dht11 sensors and device 3 has only one dht11 sensor


def on_connect(client, userdata, flags, rc):
    try: # logging added in version 139
        print('Connected with result code {0}'.format(rc))
        connect = rc
        pickle.dump( connect, open( "connect.p", "wb" ) )
        client.subscribe('temp_humidity_from_livingroom')
        client.subscribe('temp_humidity_from_kitchen')
        client.subscribe('temp_humidity_bedroom')
        return client, userdata
    except Exception as e:
        connections_logger.exception("Cannot setup the connection to mqtt: %s", e)

def timeflag(): # time rule function
    t_flag = time.time()
    return t_flag
    
    
def timestamp(): # this is for database
    timest = dt.datetime.now()
    timest = timest.strftime("%y-%m-%d %H:%M:%S")
    return timest
    


# Callback fires when a published message is received.
def on_message(client, userdata, msg): #mqtt message from living room
    temp_lux =1
    client.on_connect = on_connect
    timest = timestamp()
    message = str(msg.payload.decode("utf-8", "ignore")) # here we decode mqtt message back to string
    message = json.loads(message) # here we change the string back to json object
    esp_json_message["livingroom_indoor_temp"] = message["livingroom temperature in"] #here we copy json message to one json message what we send to main program
    esp_json_message["livingroom_indoor_humidity"] = message["livingroom humidity in"]
    esp_json_message["livingroom_outside_temp"] = message["livingroom temperature out"]
    esp_json_message["livingroom_outside_humidity"] = message["livingroom humidity out"]
    temp_lux = int(message["lux analog value livingroom"])
    if temp_lux==0:
        temp_lux=100
    print(temp_lux)
    esp_json_message["lux_value_livingroom"] = message["lux analog value livingroom"]#((4096 - temp_lux)*10) /temp_lux  
    esp_json_message["livingroom_timestamp"] = timest 
    check_devices_and_send_database()
    sendmessage()#lets check if time rule is full. then we send to main program the message
   

    
    
def on_message2(client, userdata, msg2): # message from kitchen esp
    temp_lux_kitchen = 1
    timest = timestamp()
    message = str(msg2.payload.decode("utf-8", "ignore")) # here we decode mqtt message back to string
    message = json.loads(message) # here we change the string back to json object
    esp_json_message["kitchen_indoor_temp"] = message["kitchen temperature in"]
    esp_json_message["kitchen_indoor_humidity"] = message["kitchen humidity in"]
    esp_json_message["kitchen_outdoor_temp"] = message["kitchen temperature out"]
    esp_json_message["kitchen_outdoor_humidity"] = message["kitchen humidity out"]
    print(int(message["Lux_value_kitchen_analog"]))
    
    if temp_lux_kitchen == 0:
        temp_lux_kitchen=100
    temp_lux_kitchen = int(message["Lux_value_kitchen_analog"])
    esp_json_message["lux_value_kitchen"] = message["Lux_value_kitchen_analog"]#((4096 - temp_lux_kitchen)*10) /temp_lux_kitchen 
    esp_json_message["kitchen_timestamp"] = timest 
    sendmessage() #lets check if time rule is full. then we send to main program the message
    check_devices_and_send_database()
        
def on_message4(client, userdata, msg9):   
    message = str(msg9.payload.decode("utf-8", "ignore")) # here we decode mqtt message back to string
    message = json.loads(message) # here we change the string back to json object
    timest = timestamp()
    esp_json_message["bedroom_temp"] = message["bedroom temperature in"]
    esp_json_message["bedroom_humidity"] = message["bedroom humidity in"]
    esp_json_message["bedroom_timestamp"] = timest
    check_devices_and_send_database()
    sendmessage()
   

def sendmessage():
    pickle.dump( esp_json_message, open( "device1.p", "wb" ) ) # here we send a esp1 device message with pickke
    
    
def check_devices_and_send_database(): # this will reboot devices if timestamp is too old. and if everything okay lets put values to the database
    try: # logging added in version 139
        global save_values_to_database
        checking = time.time()
        
        if checking - save_values_to_database >= 3600:#00
            save_sensors_value(esp_json_message)
            save_values_to_database = time.time()
            print("trying to save values to db")
    
    except Exception as e:
        connections_logger.exception("Cannot connect to database: %s", e)



def _start_shutdown_thread():
    def worker():
        try:
            connections_logger.info("Shutdown thread: aloitetaan plug_off-sekvenssi")
            plug_off()   # olemassa oleva funktio hoitaa varsinaisen sammuttamisen
        except Exception:
            connections_logger.exception("Shutdown thread: virhe plug_off-sekvenssissä")
    t = threading.Thread(target=worker, daemon=True)
    t.start()

@app.route("/shutdown", methods=["POST"])
def http_shutdown():
    # odotetaan JSONia, mutta ei tehdä monimutkaista validointia
    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        connections_logger.exception("Virhe lukemassa JSONia")
        return jsonify({"ok": False, "error": "invalid_json"}), 400

    if data.get("cmd") != "shutdown":
        return jsonify({"ok": False, "error": "invalid_cmd"}), 400

    connections_logger.info("HTTP shutdown: vastaanotettu, käynnistetään sekvenssi")
    _start_shutdown_thread()
    return jsonify({"ok": True, "message": "shutdown started"}), 202

    
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.message_callback_add('temp_humidity_from_livingroom', on_message)
mqtt_client.message_callback_add('temp_humidity_from_kitchen', on_message2)
mqtt_client.message_callback_add('temp_humidity_from_bedroom', on_message4)
mqtt_client.connect('localhost', 1883, 60)
mqtt_client.loop_start()

def run_shutdown_server():#version 140
    # kutsu tätä vain paikallisesti, esim. jos käytät pm2: pm2 start connections.py --interpreter python3
    app.run(host="127.0.0.1", port=5000, debug=False)


if __name__ == "__main__":
    # Jos haluat, voit ajaa Flaskin erillisessä säikeessä, mutta yleensä
    # loop_start() + app.run() on riittävä ja yksinkertainen.
    run_shutdown_server()