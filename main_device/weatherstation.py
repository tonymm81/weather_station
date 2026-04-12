import paho.mqtt.client as mqtt # c
from tkinter import *
from tkinter import messagebox
import datetime as dt #c
from database import * #c
from forecast import *
import time
from decimal import *
from PIL import ImageTk, Image
import RPi.GPIO as GPIO
from shutdown import *
from dbsearch import history
import pickle
#this is because cpu and mem test
import psutil
# here is a global variables what defines when we save the sensor data to database.
from urllib.request import urlopen
import urllib.request
import base64
import io

import logging
from logging.handlers import RotatingFileHandler
import os
import threading

LOGDIR = '/var/log/weather_station' # logging added in version 139
os.makedirs(LOGDIR, exist_ok=True)
_update_running = False
UPDATE_INTERVAL_MS = 1500
LOGDIR = '/var/log/weather_station'
SetupGpio = False
os.makedirs(LOGDIR, exist_ok=True)

def thread_wrapper(fn, *args, **kwargs): #added in version 139
    """Käynnistä fn säikeessä ja loggaa poikkeukset."""
    def run():
        try:
            fn(*args, **kwargs)
        except Exception:
            logging.exception("Exception in background thread for %s", getattr(fn, "__name__", str(fn)))
    t = threading.Thread(target=run, daemon=True)
    t.start()
    return t

def safe_call_in_mainthread(fn, *args, **kwargs):
    """Aseta funktio suoritettavaksi pääsäikeessä root.after(0,...)."""
    root.after(0, lambda: fn(*args, **kwargs))

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

# weatherstation-specific logger
weather_logger = make_logger(
    'weather.weatherstation',
    os.path.join(LOGDIR, 'weatherstation.log'),
    level=logging.INFO
)

weather_logger.info('Weatherstation logger initialized', extra={'component': 'weatherstation'})

power_on = 1
device1_time = time.time() # this are the time rule global time what we update when the time rule is true
connected_time = time.time()
answ = 0
avg_time = time.time()
forecast_time = time.time()
esp1_message = {}



def get_message1():
    global esp1_message
    time.sleep(0.1)
    try: # when i test pickle i run out errors what was typical. so i made a try except block
        esp1_message = pickle.load( open( "device1.p", "rb" ) ) # here we load message what is from connections.py with pickle
        weather_logger.debug("Loaded device1.p successfully", extra={'component':'weatherstation'})
        return esp1_message
                   
    except FileNotFoundError:
        weather_logger.warning("device1.p not found, returning empty dict", extra={'component':'weatherstation'})
        esp1_message = {}
        return esp1_message
            
    except EOFError:
        esp1_message = {}
        weather_logger.warning("device1.p EOFError, returning empty dict", extra={'component':'weatherstation'})
        return esp1_message
    except Exception:
        esp1_message = {}
        weather_logger.exception("Unexpected error loading device1.p, returning empty dict", extra={'component':'weatherstation'})
        return esp1_message
    
def get_message_4():
    time.sleep(0.1)
    connected = 0
    try:
        connected = pickle.load( open( "connect.p", "rb" ) ) # here we load message what is from connections.py with pickle
        weather_logger.debug("Loaded connect.p successfully, connected=%s", connected, extra={'component':'weatherstation'})
        return connected
    
    except FileNotFoundError:
        weather_logger.warning("connect.p not found, returning 0", extra={'component':'weatherstation'})
        connected = 0
        return connected
            
    except EOFError:
        connected = 0
        weather_logger.warning("connect.p EOFError, returning 0", extra={'component':'weatherstation'})
        return connected
    except Exception:
        connected = 0
        weather_logger.exception("Unexpected error loading connect.p, returning 0", extra={'component':'weatherstation'})
        return connected
    
    
def get_psu_mem():
    psu_state = psutil.cpu_percent()
    virtual_mem = psutil.virtual_memory() [0] # physical memory usage
    virtual_used = psutil.virtual_memory()[1]
    return psu_state, virtual_mem, virtual_used
    


def update_ui():
    global connected_time
    global device1_time
    global avg_time
    global answ
    global _update_running
    global SetupGpio
    if _update_running:
        root.after(UPDATE_INTERVAL_MS, update_ui)
        return
    _update_running = True
    reseted = False
    if SetupGpio == False:
        gpio_pins()
        SetupGpio = True
    get_message1()
    resetrule = time.time()
    
    timenow = timeflag()
    if timenow - connected_time > 15:
        answ = get_message_4()
        connected_time = time.time()
    
    if answ == "0" or answ == 0:
        answ = str(answ) 
        welcome.set(" welcome to weatherstation and we are connected  " + answ)
        
    else:
        answ = str(answ) 
        welcome.set(" welcome to weatherstation and we are not connected and " + answ + "is a error code")
            
    try: 
        if reseted ==True: # this should reset esp board if not online
            if timenow - time.mktime(dt.datetime.strptime(esp1_message["livingroom_timestamp"],"%y-%m-%d %H:%M:%S").timetuple()) > 180:
                reset_esp_boards("livingroom")
                reseted = False
                resetrule = time.time()
            elif timenow - time.mktime(dt.datetime.strptime(esp1_message["kitchen_timestamp"],"%y-%m-%d %H:%M:%S").timetuple()) >180:
                reset_esp_boards("kitchen")
                reseted = False
                resetrule = time.time()
            elif timenow - time.mktime(dt.datetime.strptime(esp1_message["bedroom_timestamp"],"%y-%m-%d %H:%M:%S").timetuple()) > 180:
                reset_esp_boards("bedroom")
                reseted = False
                resetrule = time.time()
            if (timenow - time.mktime(dt.datetime.strptime(esp1_message["bedroom_timestamp"],"%y-%m-%d %H:%M:%S").timetuple()) > 480 
                and timenow - time.mktime(dt.datetime.strptime(esp1_message["kitchen_timestamp"],"%y-%m-%d %H:%M:%S").timetuple()) >480 
                and timenow - time.mktime(dt.datetime.strptime(esp1_message["livingroom_timestamp"],"%y-%m-%d %H:%M:%S").timetuple()) > 480):
                reboot_connections() #here we startup the connections.py if its offline
                reseted = False
    except KeyError:
        print("Having errorhandling keyerror")
        weather_logger.exception("Giving the key error from line 153", extra={'component':'weatherstation'})

       
    if timenow - device1_time > 15:  # here is small timerule
        device1_measurements = get_message1()
        device1_time = time.time()
        # in labels i make big change. i delete here like over 100 lines of code.  
    if timenow - resetrule > 360:
        reseted = True
        resetrule = time.time()
    try:
           
        screen1.set(str(esp1_message["livingroom_timestamp"]) + " temperature living room is " + str(esp1_message["livingroom_indoor_temp"]) + " humidity is "+str(  esp1_message["livingroom_indoor_humidity"]))
        screen2.set(str(esp1_message["livingroom_timestamp"]) + " temperature living room outside is " + str(esp1_message["livingroom_outside_temp"]) + "  humidity is " + str(esp1_message["livingroom_outside_humidity"]))
        screen3.set(str(esp1_message["kitchen_timestamp"]) + " temperature in kitchen is " + str(esp1_message["kitchen_indoor_temp"]) + "  humidity is " + str(esp1_message["kitchen_indoor_humidity"]))
        screen4.set(str(esp1_message["kitchen_timestamp"]) + " temperature in outside kitchen is " + str(esp1_message["kitchen_outdoor_temp"]) + " humidity is " + str(esp1_message["kitchen_outdoor_humidity"]))
        screen5.set(str(esp1_message["bedroom_timestamp"]) + " temperature in bedroom is " + str(esp1_message["bedroom_temp"]) + " humidity is " + str(esp1_message["bedroom_humidity"]))
        screen6.set( "Lux value in kitchen is " + str(esp1_message["lux_value_kitchen"])+ " Living room lux value is: " + str(esp1_message["lux_value_livingroom"]))
        root.update()
        if timenow - avg_time > 3600:
            avg_display()
            avg_time = time.time()
         
        # this is temporary cpu and memory usage gauge   
        psu_state, mem_state, memory = get_psu_mem()
        psu_text.set(f"psu present = {psu_state}, virtual memory = {mem_state}, memory now = {memory}")
        #root.update()
        time.sleep(1.5)
    except KeyError:
        print("value missing")
        screen6.set("some values are missing...")
        weather_logger.exception("some values are missing...", extra={'component':'weatherstation'})

    finally:
        _update_running = False
        # ajoita seuraava päivitys
        root.after(UPDATE_INTERVAL_MS, update_ui)
        

def timeflag(): # time rule function
    t_flag = time.time()
    return t_flag
    
    
def timestamp(): # this is for database
    timest = dt.datetime.now()
    timest = timest.strftime("%y-%m-%d %H:%M:%S")
    return timest
    

def avg_display():
    """
    Turvallinen versio: laskee keskiarvot taustasäikeessä ja päivittää UI:n pääsäikeessä.
    Ei luo widgettejä eikä kutsu root.update() tai time.sleep().
    """
    logging.info("avg_display called")

    def worker():
        try:
            # Raskaat laskelmat taustasäikeessä
            living_in_avg, living_out_avg, kitchen_in_avg, kitchen_out_avg = average()
            # ota viimeisimmät arvot turvallisesti
            try:
                avg_livingroom = living_in_avg[-1][0]
            except Exception:
                avg_livingroom = "N/A"
            try:
                avg_livingroom_out = living_out_avg[-1][0]
            except Exception:
                avg_livingroom_out = "N/A"
            try:
                avg_kitchen = kitchen_in_avg[-1][0]
            except Exception:
                avg_kitchen = "N/A"
            try:
                avg_kitchen_out = kitchen_out_avg[-1][0]
            except Exception:
                avg_kitchen_out = "N/A"

            # laske hedgehog‑arvot (voi olla raskas)
            try:
                run = hedge_24h()
                total = sum(t[0] for t in run) if run else 0
                total1 = '{:.2f}'.format(total * 1.14)
            except Exception:
                logging.exception("hedge_24h failed")
                total1 = "N/A"

            # Päivitä UI pääsäikeessä
            def update_labels():
                try:
                    avg_label_living.config(text=f"average per week living room is {avg_livingroom}c. and outside {avg_livingroom_out}c.")
                    avg_label_kitchen.config(text=f"average per week kitchen is {avg_kitchen}c. and outside {avg_kitchen_out}c. Total: {total1}")
                except Exception:
                    logging.exception("Failed to update avg labels")

            safe_call_in_mainthread(update_labels)

            # Jos power_on on 1, käynnistä plug_on taustasäikeessä ja nollaa lippu pääsäikeessä
            try:
                if globals().get("power_on", 0) == 1:
                    logging.info("power_on detected, calling plug_on in background")
                    thread_wrapper(plug_on)
                    # nollataan lipun arvo pääsäikeessä
                    def clear_power_on():
                        globals()["power_on"] = 0
                    safe_call_in_mainthread(clear_power_on)
            except Exception:
                logging.exception("Error handling power_on")
        except Exception:
            logging.exception("Exception in avg_display worker")

    # käynnistä taustasäie
    thread_wrapper(worker)

def getIconUrl(code):
    
    try:
        print("try to open", code)
        
        image1 = Image.open('/home/pi/Desktop/new/new_weatherstation/main_device/icons/'+code+'.png') # rain
        image1 = image1.resize((20, 20))
        image1 = ImageTk.PhotoImage(image1, size=-3000)#-5000enne
        #image1 = image1.subsample(1,2)
    except Exception as error:
        print(str(error))
        weather_logger.exception("Error to getting icon from url", extra={'component':'weatherstation'})
    return image1
       

def ask_forecast(): # modified in version 139
    try:
        Forecast = fore_cast()  # oletetaan että tämä palauttaa listan kuten ennen
        icons = [Forecast[3], Forecast[7], Forecast[11], Forecast[15], Forecast[19]]
        texts = [
            f"next 5 day forecast is: {Forecast[0]} {Forecast[1]}c. Time: {Forecast[2]}",
            f"{Forecast[4]} {Forecast[5]}c. Time: {Forecast[6]}",
            f"{Forecast[8]} {Forecast[9]}c. Time: {Forecast[10]}",
            f"{Forecast[12]} {Forecast[13]}c. Time: {Forecast[14]}",
            f"{Forecast[16]} {Forecast[17]}c. Time: {Forecast[18]}"
        ]
    except Exception:
        # jos fore_cast epäonnistuu, älä riko UI:ta
        return

    for i, code in enumerate(icons):
        try:
            img = Image.open(f'/home/pi/Desktop/new/new_weatherstation/main_device/icons/{code}.png').resize((24,24))
            photo = ImageTk.PhotoImage(img)
            icon_labels[i].config(image=photo)
            icon_labels[i].image = photo   # tallenna viite estääksesi GC:n
        except Exception:
            icon_labels[i].config(image='')  # placeholder tai tyhjä

        forecast_labels[i].config(text=texts[i])
    
 
def shutdownmachine(inputpin):
    inp = GPIO.input(26)
    if inp == 1:
        plug_off() # here we shutdown the remote plugs and hedgehogs counter from shutdown.py
    
    
    
def gpio_pins():
# and for sure here is gpio setup. same setup found also in shutdown.py
    inputpin = 26
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(inputpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    try:
        GPIO.add_event_detect(inputpin, GPIO.FALLING, callback=shutdownmachine) # if shutdown pressed, we go to function shutdownmachine
        
    except RuntimeError:
        GPIO.remove_event_detect(inputpin)
        GPIO.cleanup(inputpin)
        inputpin = 26
        GPIO.setup(inputpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(inputpin, GPIO.FALLING, callback=shutdownmachine)
        weather_logger.exception("Error in gpio handling", extra={'component':'weatherstation'})
        
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
    inputpin = GPIO.input(26)



root = Tk()
os.environ["DISPLAY"] = ":0"
root.title('weather station')
root.geometry("800x480")
root.configure(background="black")
root.grid_columnconfigure(0, weight=0, minsize=60) # added in version 139
root.grid_columnconfigure(1, weight=1, minsize=600)
# forecast function images here
img1=""
img2=""
img3=""
img4=""
img5 = ""
image1 = ""
screen1 = StringVar(); screen2 = StringVar(); screen3 = StringVar()
screen4 = StringVar(); screen5 = StringVar(); screen6 = StringVar()
psu_text = StringVar()# added to psu own label
welcome = StringVar()
#screen1,screen2, screen3, screen4, screen5, screen6.set("")
FONT_MAIN = ("helvetica", 11)
FONT_SMALL = ("helvetica", 10)
# chancing the label variables in version 139
livingroom_in = Label(root, textvariable=screen1, font=("Helvetica",12), fg="lightcyan", bg="black", anchor="w", justify="left", wraplength=600)
livingroom_in.grid(row=2, column=1, sticky="w", padx=8, pady=2)
livingroom_out = Label(root, textvariable=screen2 , font=("helvetica", 12), fg="white", bg="black")
livingroom_out.grid(row=4, column=1, sticky="w", padx=8, pady=2)
kitchen_in = Label(root, textvariable=screen3 , font=("helvetica", 12), fg="white", bg="black")
kitchen_in.grid(row=6, column=1, sticky="w", padx=8, pady=2)
kitchen_out = Label(root, textvariable= screen4, font=("helvetica", 12), fg="white", bg="black")
kitchen_out.grid(row=8, column=1, sticky="w", padx=8, pady=2)
bedroom = Label(root, textvariable= screen5, font=("helvetica", 12), fg="white", bg="black") # remember row
bedroom.grid(row=10, column=1, sticky="w", padx=8, pady=2)
lux_values = Label(root, textvariable= screen6  ,  font=("helvetica", 12), fg="white", bg="black")
lux_values.grid(row=14, column=1, sticky="w", padx=8, pady=2)
welcome_label = Label(root, textvariable=welcome,  font=("helvetica", 12), fg="green", bg="black")
welcome_label.grid(row=0, column=1, sticky="w", padx=8, pady=2) #if we have connection, then the text is green
psu_label = Label(root, textvariable=psu_text, font=("Helvetica",10), fg="lightgrey", bg="black", anchor="w", wraplength=600)
psu_label.grid(row=40, column=1, sticky="w", padx=8, pady=2)      # added to psu own label

avg_label_living = Label(root, text="", font=("Helvetica", 10), fg="white", bg="black", anchor="w", justify="left", wraplength=600)
avg_label_living.grid(row=16, column=1, sticky="w", padx=8, pady=2) #moved avg labels here version 139

avg_label_kitchen = Label(root, text="", font=("Helvetica", 10), fg="white", bg="black", anchor="w", justify="left", wraplength=600)
avg_label_kitchen.grid(row=18, column=1, sticky="w", padx=8, pady=2)

# here is program buttons 
btn_frame = Frame(root, bg="black")# modified on version 139
btn_frame.grid(row=30, column=1, sticky="w", padx=8, pady=2)

# Nappien luonti ja pack vaakariviksi
btn = Button(btn_frame, text="view history", fg="white", bg="black", font=("Helvetica", 10), command=history, width=18)
btn.pack(side="left", padx=6)

btn6 = Button(btn_frame, text="update the forecast view here", fg="white", bg="black", font=("Helvetica", 10), command=ask_forecast, width=30)
btn6.pack(side="left", padx=6)

btn8 = Button(btn_frame, text="restart esp boards", fg="white", bg="black", font=("Helvetica", 10), command=reset_esp_boards, width=18)
btn8.pack(side="left", padx=6)

icon_labels = [] # modified in version 139
forecast_labels = []
for i, r in enumerate([20,22,24,26,28]):
    il = Label(root, bg="black")
    il.grid(row=r, column=0, padx=4, pady=2)
    icon_labels.append(il)
    fl = Label(root, text="", font=("Helvetica",10), fg="white", bg="black", anchor="w", justify="left", wraplength=600)
    fl.grid(row=r, column=1, sticky="w", padx=8, pady=2)
    forecast_labels.append(fl)




ask_forecast()
avg_display()
#gpio_pins()
root.after(0, update_ui)
root.mainloop()
