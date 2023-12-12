from subprocess import call
import subprocess
from sys import stdout
import time
import RPi.GPIO as GPIO
from broadlink_control.broadlink_switch import *
import random
#from broadlink_control.pswd import *


valo1 = 19
valo2 = 13
valo3 = 6
on_off_vaihto = 5
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#GPIO.setup(inputpin, GPIO.IN, pull_up_down=GPIO.PUD_UP) #
GPIO.setup(valo1, GPIO.OUT)
GPIO.setup(valo2, GPIO.OUT)
GPIO.setup(valo3, GPIO.OUT)
GPIO.setup(on_off_vaihto, GPIO.OUT)


def shutdown(): # here we shutdown the weatherstation
    time.sleep(1.0)
    
    call("sudo shutdown -h now", shell=True)
    
    
def reboot_connections():
    call("./sudo python3 connections.py &", shell=True)
    reset_esp_boards("all")
    #print(stdout())
    #subprocess.Popen(["sudo python3 /home/pi/Desktop/new/new_weatherstation/main_device/connections.py"]) #"rm","-r",
    
    
def plug_on(): # here we power up the esp board and hedgehogs spinning wheelcounter powers.
    broadlink_switch_control("on", "all")
    i = 0
    o = 0
    io = 12#random.uniform(4, 14)
    delay_relays= 0.01#random.uniform((0.09, 0.0006),2)
    while True:
        GPIO.output(valo1, GPIO.HIGH)
        time.sleep(delay_relays)
        GPIO.output(valo1, GPIO.LOW)
        for i in range(io):
            #delay_relays= random.uniform((0.09, 0.0006),2)
            time.sleep(delay_relays)
            GPIO.output(valo2, GPIO.HIGH)
            time.sleep(delay_relays)
            GPIO.output(valo2, GPIO.LOW)
            time.sleep(delay_relays)
            GPIO.output(valo3, GPIO.HIGH)
            time.sleep(delay_relays)
            GPIO.output(valo3, GPIO.LOW)
            time.sleep(delay_relays)
            GPIO.output(valo1, GPIO.HIGH)
            time.sleep(delay_relays)
            GPIO.output(valo1, GPIO.LOW)
            i = 1 +1
            for o in range (7):
                GPIO.output(valo1, GPIO.HIGH)
                time.sleep(delay_relays)
                GPIO.output(valo1, GPIO.LOW)
                o = o +1
        
        break
    return
    
    
def plug_off(): # here we power off the esp board and hedgehogs spinning wheelcounter powers. planning here wlan plugs but working on it.
    broadlink_switch_control("off", "all")
    i = 0
    o = 0
    while True:
        GPIO.output(valo1, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(valo1, GPIO.LOW)
        for i in range(12):
            time.sleep(0.05)
            GPIO.output(valo2, GPIO.HIGH)
            time.sleep(0.01)
            GPIO.output(valo2, GPIO.LOW)
            time.sleep(0.05)
            GPIO.output(valo3, GPIO.HIGH)
            time.sleep(0.01)
            GPIO.output(valo3, GPIO.LOW)
            time.sleep(0.05)
            GPIO.output(valo1, GPIO.HIGH)
            time.sleep(0.01)
            GPIO.output(valo1, GPIO.LOW)
            i = 1 +1
            for o in range (8):
                GPIO.output(valo1, GPIO.HIGH)
                time.sleep(0.001)
                GPIO.output(valo1, GPIO.LOW)
                o = o +1
        
        break
    shutdown()
    
    
def reset_esp_boards(what_device):
    broadlink_switch_control("on", what_device)
    broadlink_switch_control("off", what_device)
    
    return
#reboot_connections()
#plug_on()