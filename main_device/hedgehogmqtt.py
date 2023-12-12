from database import *
import paho.mqtt.client as mqtt
import datetime as dt
import struct

def timestamp():
    timest = dt.datetime.now()
    timest = timest.strftime("%y-%m-%d %H:%M:%S")
    timest = str(timest) # tkinter requires the str value
    return timest



def on_connect5(client1, userdata, flags, rc): # here we define the connection and tell mqtt client id
    print('Connected with result code {0}'.format(rc))
    client1.subscribe('hedgehogsrun')

def on_message5(client1, userdata, msg5): #this is for hedgehogs runnings when the laskuriapi.py takes connections
    hedge_run = [str(x) for x in msg5.payload.decode("utf-8").split(',')]
    print("message is here")
    timest = timestamp()
    hedge_run = hedge_run[0]
    print(hedge_run)
    hedgehog1(hedge_run, timest) #to database
    answer = 0
    msg6 = answer
    print("send back")
    
    
 
# his 1could be cliet1 what is made to hedgehogs counter
client1 = mqtt.Client()
client1.on_connect = on_connect5  # Specify on_connect callback
#client1.on_message = on_message5 # Specify on_message callback
client1.connect('localhost', 1883, 60)# Connect to MQTT broker (also running on Pi).
client1.message_callback_add('hedgehogsrun', on_message5)  
client1.loop_forever() #  Processes MQTT network traffic, callbacks and reconnections. (Blocking)

