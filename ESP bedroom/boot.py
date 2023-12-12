from time import sleep
from umqtt.simple import MQTTClient

from machine import Pin
import dht
import json
import network
import os
import esp
esp.osdebug(None)




ssid = ''
password = ''
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())


SERVER = '192.168.68.200'  # MQTT Server Address (Change to the IP address of your Pi) remember to check
CLIENT_ID = 'ESP32_DHT11_Sensor_bedroom'
TOPIC9 = b'temp_humidity_bedroom' # update this on microcontroller!!!!
 

client = MQTTClient(CLIENT_ID, SERVER)
client.connect()   # Connect to MQTT broker

sensor9 = dht.DHT11(Pin(14))   # DHT-11 on GPIO 15 (input with internal pull-up resistor)




while True:
    try:
        
        sensor9.measure()   # Poll sensor1
        temp_in = sensor9.temperature()
        hum_in = sensor9.humidity()
        
        if (isinstance(temp_in, float) and isinstance(hum_in, float)) or (isinstance(temp_in, int) and isinstance(hum_in, int)): 
            message = {"bedroom temperature in": ""+temp_in+"", "bedroom humidity in": ""+hum_in+""} #lets packup message to json string
            msg9 = json.dumps(message)
            client.publish(TOPIC9, msg9)  # Publish sensor data to MQTT topic
            
        else:
            print('Invalid sensor readings.')
          
            #client.publish(TOPIC, msg, msg1)
    except OSError:
        print('Failed to read sensor.')
    sleep(15)