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
        return esp1_message
                   
    except FileNotFoundError:
        esp1_message = {}
        return esp1_message
            
    except EOFError:
        esp1_message = {}
        return esp1_message
    
    
def get_message_4():
    time.sleep(0.1)
    connected = 0
    try:
        connected = pickle.load( open( "connect.p", "rb" ) ) # here we load message what is from connections.py with pickle
        return connected
    
    except FileNotFoundError:
        connected = 0
        return connected
            
    except EOFError:
        connected = 0
        return connected
    
    
def get_psu_mem():
    psu_state = psutil.cpu_percent()
    virtual_mem = psutil.virtual_memory() [0] # physical memory usage
    virtual_used = psutil.virtual_memory()[1]
    return psu_state, virtual_mem, virtual_used
    


def mainloop():
    global connected_time
    global device1_time
    global avg_time
    global answ
    reseted = False
    gpio_pins()
    get_message1()
    resetrule = time.time()
    while True:
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
            screen6.set( "Lux value in kitchen is" + str(esp1_message["lux_value_kitchen"])+ " Living room lux value is: " + str(esp1_message["lux_value_livingroom"]))
            root.update()
            if timenow - avg_time > 3600:
                avg_display()
                avg_time = time.time()
         
        # this is temporary cpu and memory usage gauge   
            psu_state, mem_state, memory = get_psu_mem()
            label_12 = Label(root, text= "psu present = "+ str(psu_state)+ " , and virtual memory= "+str(mem_state)+" , memory now = "+str(memory)  ,  font=("helvetica", 20), fg="white", bg="black")
            label_12.grid(row=40, column=1)
            label_12.destroy()
            root.update()
            time.sleep(1.5)
        except KeyError:
            print("value missing")
            screen6.set("some values are missing...")
            time.sleep(1)
        
def timeflag(): # time rule function
    t_flag = time.time()
    return t_flag
    
    
def timestamp(): # this is for database
    timest = dt.datetime.now()
    timest = timest.strftime("%y-%m-%d %H:%M:%S")
    return timest
    

def avg_display():
    global avg0, avg1, avg3, avg4
    global power_on
    print("asking avg")
    
    living_in_avg, living_out_avg, kitchen_in_avg, kitchen_out_avg = average()
    avg_livingroom = living_in_avg[-1]
    avg_livingroom_out = living_out_avg[-1]
    avg_kitchen = kitchen_in_avg[-1]
    avg_kitchen_out = kitchen_out_avg[-1]
    label_14 = Label(root, text= " average per week living room is " + str(avg_livingroom[0]) + "c." + " and outside " + str(avg_livingroom_out[0]) + "c." ,  font=("helvetica", 25), fg="white", bg="black")
    label_14.grid(row=16, column=1, )
    label_6 = Label(root, text= " average per week kitchen is " + str(avg_kitchen[0])  + "c." + " and outside " + str(avg_kitchen_out[0]) + "c.",  font=("helvetica", 25), fg="white", bg="black")
    label_6.grid(row=18, column=1)
    root.update()
    run = hedge_24h()
    #print(run[0])
    day_run = 0
    total = sum(t[0] for t in run)
    #print(total)
    total1 = total * 1.14
    total1 = '{:.2f}'.format(total1)
    label_15 = Label(root, text= "hedgehogs runnings from 24 hours is: " + str(total) + " rounds, and in meters : " + str(total1),  font=("helvetica", 25), fg="white", bg="black")
    label_15.grid(row=12, column=1)
    
    root.update()
    if power_on == 1: #here we power on the esp boards and hedgehogs counter
        plug_on()
        power_on = 0

def getIconUrl(code):
    
    try:
        print("try to open", code)
        
        image1 = Image.open('/home/pi/Desktop/new/new_weatherstation/main_device/icons/'+code+'.png') # rain
        image1 = image1.resize((60, 60))
        image1 = ImageTk.PhotoImage(image1, size=-3000)#-5000enne
        #image1 = image1.subsample(1,2)
    except Exception as error:
        print(str(error))
    return image1
       

def ask_forecast():
    global image1
    global img1, img2, img3 ,img4, img5
    print("asking forecAst")
    Forecast = []
    Forecast = fore_cast() #here we call the forecast.py function and this function returns a list where i digout the data
    time.sleep(2)
    print(Forecast)
    img5=getIconUrl(Forecast[3]) # here we get the right image what is in desscription
    img4=getIconUrl(Forecast[7])
    img3=getIconUrl(Forecast[11])
    img2=getIconUrl(Forecast[15])
    img1=getIconUrl(Forecast[19])
    #print(Forecast[x])
    label_7 = Label(root, text= "next 5 day forecast is: " + Forecast[0] + " " +  str(Forecast[1]) + "c. Time: " + str(Forecast[2])  ,  font=("helvetica", 20), fg="white", bg="black")
    label_7.grid(row=20, column=1, )
    imagebutton = Button(root, image=img5) # this button was only way to add image on text line, iam not sure is there better way to do this
    imagebutton.grid(row=20, column=0, pady=0, padx=0, ipadx=0)
    label_8 = Label(root, text= str(Forecast[4]) + " " + str(Forecast[5]) + "c. Time: " + str(Forecast[6]) ,  font=("helvetica", 20), fg="white", bg="black")
    label_8.grid(row=22, column=1)
    imagebutton1 = Button(root, image=img4)
    imagebutton1.grid(row=22, column=0, pady=0, padx=0, ipadx=0)
    label_9 = Label(root, text= str(Forecast[8])  + " " + str(Forecast[9]) + "c. Time: " + str(Forecast[10])   ,  font=("helvetica", 20), fg="white", bg="black")
    label_9.grid(row=24, column=1)
    imagebutton2 = Button(root, image=img3)
    imagebutton2.grid(row=24, column=0, pady=0, padx=0, ipadx=0)
    label_10 = Label(root, text= str(Forecast[12])+ " " + str(Forecast[13]) + "c. Time: " + str(Forecast[14])  ,  font=("helvetica", 20), fg="white", bg="black")
    label_10.grid(row=26, column=1)
    imagebutton3 = Button(root, image=img2)
    imagebutton3.grid(row=26, column=0, pady=0, padx=0, ipadx=0)
    label_11 = Label(root, text= str(Forecast[16])+ " " + str(Forecast[17]) + "c. Time: " +str(Forecast[18]) ,  font=("helvetica", 20), fg="white", bg="black")
    label_11.grid(row=28, column=1)
    imagebutton4 = Button(root, image=img1)
    imagebutton4.grid(row=28, column=0, pady=0, padx=0, ipadx=0)
    
    root.update()
    
 
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
root.title('weather station')
root.geometry("1900x1080")
root.configure(background="black")
# forecast function images here
img1=""
img2=""
img3=""
img4=""
img5 = ""
image1 = ""
screen1 = StringVar("")
screen2 = StringVar("")
screen3 = StringVar("")
screen4 = StringVar("")
screen5 = StringVar("")
screen6 = StringVar("")
welcome = StringVar("")
#screen1,screen2, screen3, screen4, screen5, screen6.set("")

livingroom_in = Label(root, textvariable= screen1 , font=("helvetica", 25), fg="white", bg="black")
livingroom_in.grid(row=2, column=1)
livingroom_out = Label(root, textvariable=screen2 , font=("helvetica", 25), fg="white", bg="black")
livingroom_out.grid(row=4, column=1)
kitchen_in = Label(root, textvariable=screen3 , font=("helvetica", 25), fg="white", bg="black")
kitchen_in.grid(row=6, column=1)
kitchen_out = Label(root, textvariable= screen4, font=("helvetica", 25), fg="white", bg="black")
kitchen_out.grid(row=8, column=1)
bedroom = Label(root, textvariable= screen5, font=("helvetica", 27), fg="white", bg="black") # remember row
bedroom.grid(row=10, column=1)
lux_values = Label(root, textvariable= screen6  ,  font=("helvetica", 25), fg="white", bg="black")
lux_values.grid(row=14, column=1)
welcome_label = Label(root, textvariable=welcome,  font=("helvetica", 30), fg="green", bg="black")
welcome_label.grid(row=0, column=1) #if we have connection, then the text is green
       
# here is program buttons 
btn = Button(root, text="view history",fg="white", bg="black",font=("helvetica", 15), command=lambda: history()).grid(row=30, column=1, pady=0, padx=0, ipadx=0) # put this to weatherstation
btn6 = Button(root, text="update the forecast view here",fg="white", bg="black",font=("helvetica", 15), command= ask_forecast).grid(row=32, column=1, pady=0, padx=0, ipadx=0)
btn7 = Button(root, text="update the database to web server",fg="white", bg="black",font=("helvetica", 15), command= lambda: history()).grid(row=34, column=1, pady=0, padx=0, ipadx=0)
btn8 = Button(root, text="restart esp boards",fg="white", bg="black",font=("helvetica", 15), command= lambda: reset_esp_boards()).grid(row=36, column=1, pady=0, padx=0, ipadx=0)

btn9 = Button(root, text="restart graphics",fg="white", bg="black",font=("helvetica", 15), command= lambda: mainloop()).grid(row=38, column=1, pady=0, padx=0, ipadx=0)
root.update()
ask_forecast()
avg_display()
#gpio_pins()
mainloop()
