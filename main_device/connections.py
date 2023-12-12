import paho.mqtt.client as mqtt #just building up connections
import datetime as dt
from database import *
import time
import pickle
import json
from shutdown import *


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
    print('Connected with result code {0}'.format(rc))
    connect = rc
    pickle.dump( connect, open( "connect.p", "wb" ) )
    client.subscribe('temp_humidity_from_livingroom') 
    client.subscribe('temp_humidity_from_kitchen')
    client.subscribe('temp_humidity_bedroom')
    return client, userdata


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
    global save_values_to_database
    checking = time.time()
    
    if checking - save_values_to_database >= 3600:#00
        save_sensors_value(esp_json_message)
        save_values_to_database = time.time()
        print("trying to save values to db")
    
    
 
 
    
client = mqtt.Client()
client.on_connect = on_connect
client.message_callback_add('temp_humidity_from_livingroom', on_message)
client.message_callback_add('temp_humidity_from_kitchen', on_message2)
client.message_callback_add('temp_humidity_bedroom', on_message4)
client.connect('localhost', 1883, 60)# Connect to MQTT broker (also running on Pi).   
client.loop_forever() #  Processes MQTT network traffic, callbacks and reconnections. (Blocking)