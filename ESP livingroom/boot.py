from time import sleep
from umqtt.simple import MQTTClient

from machine import Pin, ADC
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
#print(station.ifconfig())


SERVER = '192.168.68.200'  # MQTT Server Address (Change to the IP address of your Pi) remember to check
CLIENT_ID = 'ESP32_DHT11_Sensor_livingroom'
TOPIC = b'temp_humidity_from_livingroom'
 

client = MQTTClient(CLIENT_ID, SERVER)
client.connect()   # Connect to MQTT broker

Living_room_in = dht.DHT11(Pin(14))   # DHT-11 on GPIO 15 (input with internal pull-up resistor)
Living_room_out = dht.DHT22(Pin(27))  #outdoor sensor
lux_sensor = ADC(Pin(35))
lux_sensor.atten(ADC.ATTN_11DB)
#station = network.WLAN(network.STA_IF)


while True:
    try:
        
        Living_room_in.measure()   # Poll sensor1
        temp_in = Living_room_in.temperature()  # lets save the value from sensor
        hum_in = Living_room_in.humidity()
        Living_room_out.measure()   # Poll sensor2
        temp_out = Living_room_out.temperature()
        hum_out = Living_room_out.humidity()
        lux_analog_value = lux_sensor.read()
        print(temp_out)
        
        if (isinstance(temp_in, float) and isinstance(hum_in, float)) or (isinstance(temp_in, int) and isinstance(hum_in, int)): # check if the sensors give proper value
            
            if (isinstance(temp_out, float) and isinstance(hum_out, float)) or (isinstance(temp_out, int) and isinstance(hum_out, int)):
                temp_in = str(temp_in)
                temp_out = str(temp_out) #convert to string that we can save this info to array
                hum_in = str(hum_in)
                hum_out = str(hum_out)
                message = {"livingroom temperature in": ""+temp_in+"", "livingroom humidity in": ""+hum_in+"",
                "livingroom temperature out": ""+temp_out+"", "livingroom humidity out": ""+hum_out+"",
                "lux analog value livingroom": ""+str(lux_analog_value)+""} #lets packup message to json string
                msg = json.dumps(message)
                client.publish(TOPIC, msg)  # Publish sensor data to MQTT topic
                
        else:
            print('Invalid sensor readings.')
            #print( msg)
    except OSError:
        print('Failed to read sensor.')
    print(msg)
    sleep(50)
