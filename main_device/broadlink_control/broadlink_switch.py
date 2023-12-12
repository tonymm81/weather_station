import broadlink # made by mjg59 
from setuptools import setup, find_packages
from broadlink import *
from broadlink import device
from broadlink import switch
import cryptography
import re
import time
#from pswd import broadlink_switch_user
esp_kitchen_str = ""
esp_bedroom_str = ""
esp_kitchen_ip = ""
esp_bedroom_ip = ""
esp_livingroom_str = ""
esp_livingroom_ip = ""


def broadlink_switch_control(position, what_device):
    global esp_kitchen_str, esp_bedroom_str, esp_kitchen_ip, esp_bedroom_ip, esp_livingroom_str, esp_livingroom_ip
    #wlan, pswd = broadlink_switch_user() 
    #broadlink.setup(wlan, pswd, 3)
    devices = broadlink.discover(timeout=5, local_ip_address='192.168.68.200')
    #print(devices)
    try:
        i = len(devices)
        o = 0
        
        for o in range (i):# broadlinkdevice could change a ip address so lets check out the ipaddress with a name and save the ip in value
            if devices[o].name == "Esp_Kitchen|1":
                esp_kitchen_str = devices[o]
                esp_kitchen_str = str(esp_kitchen_str)
                result = re.findall(r'[\d\.]+', esp_kitchen_str)
                esp_kitchen_ip = result[5]#this works on sp3-eu plugs and [4] works with sp4-eu
        
            if devices[o].name == "Esp_Bedroom|1":
                esp_bedroom_str = devices[o]
                esp_bedroom_str = str(esp_bedroom_str)
                result1 = re.findall(r'[\d\.]+', esp_bedroom_str)
                esp_bedroom_ip = result1[5]#this works on sp3-eu plugs and [4] works with sp4-eu
                
            if devices[o].name == "Esp_livingroom|1":
                esp_livingroom_str = devices[o]
                esp_livingroom_str = str(esp_livingroom_str)
                result2 = re.findall(r'[\d\.]+', esp_livingroom_str)
                esp_livingroom_ip = result2[5]#this works on sp3-eu plugs and [4] works with sp4-eu
                print(esp_livingroom_ip)
            o = + 1
            
    except IndexError: #when the devices is somehow offline and the result is false lets continue the program
        return
    
    
    devices_kitchen = broadlink.discover(timeout=5, discover_ip_address=esp_kitchen_ip) 
    devices_bedroom = broadlink.discover(timeout=5, discover_ip_address=esp_bedroom_ip)
    devices_livingroom = broadlink.discover(timeout=5, discover_ip_address=esp_livingroom_ip)
    devices_kitchen[0].auth()
    devices_bedroom[0].auth()
    devices_livingroom[0].auth()
    state_kitchen = devices_kitchen[0].check_power()
    state_bedroom = devices_bedroom[0].check_power()
    state_livingroom = devices_livingroom[0].check_power()

    if position == "on":
        
        if state_kitchen == False and what_device == "kitchen" or what_device == "all":
            devices_kitchen[0].set_power(True)
            time.sleep(1)
            
        if state_bedroom == False and what_device == "bedroom" or what_device == "all":
            devices_bedroom[0].set_power(True)
            time.sleep(1)
            
        if state_livingroom == False and what_device == "livingroom" or what_device == "all":
            devices_livingroom[0].set_power(True)
            time.sleep(1)
    
    
    
    elif position == "off":
        if state_kitchen == True and what_device == "kitchen" or what_device == "all":
            devices_kitchen[0].set_power(False)
            time.sleep(1)
            
        if state_bedroom == True and what_device == "bedroom" or what_device == "all":
            devices_bedroom[0].set_power(False)
            time.sleep(1)
            
        if state_livingroom == True and what_device == "livingroom" or what_device == "all":
            devices_livingroom[0].set_power(False)
            time.sleep(1)
        
    
    
    return
    
    


position = "on"
broadlink_switch_control(position, "all")