import broadlink # made by mjg59 
from setuptools import setup, find_packages
from broadlink import *
from broadlink import device
from broadlink import switch
import cryptography
import re
import time
import logging
from logging.handlers import RotatingFileHandler
import os
#from pswd import broadlink_switch_user
esp_kitchen_str = ""
esp_bedroom_str = ""
esp_kitchen_ip = ""
esp_bedroom_ip = ""
esp_livingroom_str = ""
esp_livingroom_ip = ""



LOGDIR = '/var/log/weather_station'  # logging added in version 139
os.makedirs(LOGDIR, exist_ok=True)

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

# broadlink-specific logger
broadlink_logger = make_logger(
    'weather.broadlink_switch',
    os.path.join(LOGDIR, 'broadlink_switch.log'),
    level=logging.INFO
)

broadlink_logger.info('Broadlink switch logger initialized', extra={'component': 'broadlink_switch'})

def broadlink_switch_control(position, what_device):
    global esp_kitchen_str, esp_bedroom_str, esp_kitchen_ip, esp_bedroom_ip, esp_livingroom_str, esp_livingroom_ip

    try:
        devices = broadlink.discover(timeout=5, local_ip_address='192.168.68.200')
        broadlink_logger.info(f"broadlink.discover called, devices={devices}")
    except Exception:
        broadlink_logger.exception("broadlink.discover epäonnistui")
        return

    if not devices:
        broadlink_logger.warning("Ei löydetty Broadlink-laitteita (devices on tyhjä tai None)")
        return

    try:
        i = len(devices)
        broadlink_logger.info(f"Löytyi {i} Broadlink-laitetta")

        for o in range(i):
            try:
                dev = devices[o]
                dev_name = getattr(dev, 'name', None)
                broadlink_logger.debug(f"Tarkastellaan laitetta index={o} name={dev_name} repr={dev!r}")
            except Exception:
                broadlink_logger.exception(f"Virhe laitetta haettaessa indexillä {o}")
                continue

            # --- KITCHEN ---
            if dev_name == "Esp_Kitchen|7":
                esp_kitchen_str = str(dev)
                try:
                    result = re.findall(r'[\d\.]+', esp_kitchen_str)
                    esp_kitchen_ip = result[5]
                    broadlink_logger.info(f"Esp_Kitchen löydetty, ip={esp_kitchen_ip}")
                except Exception:
                    broadlink_logger.exception(f"Esp_Kitchen: IP-extract epäonnistui, repr={esp_kitchen_str}")

            # --- BEDROOM ---
            if dev_name == "Esp_Bedroom|7":
                esp_bedroom_str = str(dev)
                try:
                    result1 = re.findall(r'[\d\.]+', esp_bedroom_str)
                    esp_bedroom_ip = result1[5]
                    broadlink_logger.info(f"Esp_Bedroom löydetty, ip={esp_bedroom_ip}")
                except Exception:
                    broadlink_logger.exception(f"Esp_Bedroom: IP-extract epäonnistui, repr={esp_bedroom_str}")

            # --- LIVINGROOM ---
            if dev_name == "Esp_livingroom|7":
                esp_livingroom_str = str(dev)
                try:
                    result2 = re.findall(r'[\d\.]+', esp_livingroom_str)
                    esp_livingroom_ip = result2[5]
                    broadlink_logger.info(f"Esp_livingroom löydetty, ip={esp_livingroom_ip}")
                except Exception:
                    broadlink_logger.exception(f"Esp_livingroom: IP-extract epäonnistui, repr={esp_livingroom_str}")

    except IndexError:
        broadlink_logger.exception("IndexError Broadlink-laitteiden käsittelyssä")
        return
    except Exception:
        broadlink_logger.exception("Tuntematon virhe Broadlink-laitteiden käsittelyssä")
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