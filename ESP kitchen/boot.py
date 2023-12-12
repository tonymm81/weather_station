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
#print(station.ifconfig())()


SERVER = '192.168.68.200'  # MQTT Server Address (Change to the IP address of your Pi) remember to check
CLIENT_ID = 'ESP32_DHT11_Sensor_kitchen'
TOPIC2 = b'temp_humidity_from_kitchen'

client = MQTTClient(CLIENT_ID, SERVER)
client.connect()   # Connect to MQTT broker

kitchen_sensor_in = dht.DHT11(Pin(14))   # DHT-11 on GPIO 15 (input with internal pull-up resistor)
kitchen_sensor_out = dht.DHT22(Pin(27))  # the outdoor sensor
lux_sensor = ADC(Pin(35))
lux_sensor.atten(ADC.ATTN_11DB)
#station = network.WLAN(network.STA_IF)


while True:
    try:
    
        kitchen_sensor_in.measure()   # Poll sensor1
        temp_in = kitchen_sensor_in.temperature() # lets save the value from sensor
        hum_in = kitchen_sensor_in.humidity()
        kitchen_sensor_out.measure()   # Poll sensor2
        temp_out = kitchen_sensor_out.temperature()
        hum_out = kitchen_sensor_out.humidity()
        lux_analog_value = lux_sensor.read()
        if (isinstance(temp_in, float) and isinstance(hum_in, float)) or (isinstance(temp_in, int) and isinstance(hum_in, int)): #lets check is the sensor given value proper
            
            if (isinstance(temp_out, float) and isinstance(hum_out, float)) or (isinstance(temp_out, int) and isinstance(hum_out, int)):
                temp_in = str(temp_in) #convert to string that we can save this info to array
                temp_out = str(temp_out)
                hum_in = str(hum_in)
                hum_out = str(hum_out)
                message = {"kitchen temperature in": ""+temp_in+"", "kitchen humidity in": ""+hum_in+"",
                "kitchen temperature out": ""+temp_out+"", "kitchen humidity out": ""+hum_out+"",
                "Lux_value_kitchen_analog": ""+str(lux_analog_value)+""} #lets packup message to json string
                msg2 = json.dumps(message)
                client.publish(TOPIC2, msg2) 
                
            
        else:
            print('Invalid sensor readings.')
            
            
    except OSError:
        print('Failed to read sensor.')
    print(msg2)
    
    sleep(50)
