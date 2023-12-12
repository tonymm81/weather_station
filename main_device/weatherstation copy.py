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
# here is a global variables what defines when we save the sensor data to database.

mess_1_timestamp = time.time() #c
mess_2_timestamp = time.time() #c
mess_3_timestamp = time.time() #c
mess_4_timestamp = time.time() #c
mess_5_timestamp = time.time() #c
power_on = 1
rc = 0

def on_connect1(client, userdata, flags, rc): # here we have a connection function #c
    print('Connected with result code {0}'.format(rc))
    
    return client, userdata

 
def on_connect(client, userdata, flags, rc): #c
    print('Connected with result code {0}'.format(rc))
    # Subscribe (or renew if reconnect).
    client.subscribe('temp_humidity') 
    client.subscribe('temp_humidity1')
    client.subscribe('temp_humidity2')
    client.subscribe('temp_humidity3')
    client.subscribe('temp_humidity_bedroom')
    
    
    
    answ = rc
    answ = str(answ) # tkinter requires the str value
    
    if rc == 0:
        label_5 = Label(root, text=" welcome to weatherstation and we are connected  " + answ,  font=("helvetica", 30), fg="green", bg="black")
        label_5.grid(row=0, column=1) #if we have connection, then the text is green
        root.update()
        
    else:
        label_5 = Label(root, text=" welcome to weatherstation and we are not connected and " + answ + "is a error code",  font=("helvetica", 30), fg="red", bg="black")
        label_5.grid(row=0, column=1)
        root.update()
        
        
    return client, userdata #c
    
    
def timeflag(): # time rule function
    t_flag = time.time()
    return t_flag
    
    
def timestamp(): # this is for database
    timest = dt.datetime.now()
    timest = timest.strftime("%y-%m-%d %H:%M:%S")
    return timest
    


# Callback fires when a published message is received.
def on_message(client, userdata, msg): #c
    global mess_1_timestamp
    t = 0
    h = 0
    client.on_connect = on_connect
    timest = timestamp()
	# Decode temperature and humidity values from binary message paylod.
    t, h = [float(x) for x in msg.payload.decode("utf-8").split(',')]
    dbflag = timeflag() #here we get the timestamp
    print(dbflag)
    if dbflag - mess_1_timestamp > 3600: # and here we calculate if the time rule is true or not
        esp1(t, h, timest) # to database
        mess_1_timestamp = timeflag() # here we set the flag nd start counting again
    timest = str(timest)
    t = str(t) # tkinter requires the str value
    h = str(h)
    label_1 = Label(root, text= timest + " temperature living room is " + t + " humidity is " + h, font=("helvetica", 25), fg="white", bg="black")
    label_1.grid(row=2, column=1)
    root.update()
    
    

    
    
def on_message1(client, userdata, msg1): #c
    global mess_2_timestamp
    
    t1 = 0
    h1 = 0 
    t1, h1 = [float(x) for x in msg1.payload.decode("utf-8").split(',')]
    dbflag = timeflag()
    timest = timestamp()
    if dbflag - mess_2_timestamp > 3600:
        esp2(t1, h1, timest)
        mess_2_timestamp = timeflag()
    timest = str(timest)
    t1 = str(t1) # tkinter requires the str value
    h1 = str(h1)
    label_2 = Label(root, text=timest + " temperature living room outside is " + t1 + "  humidity is " + h1, font=("helvetica", 25), fg="white", bg="black")
    label_2.grid(row=4, column=1)
    t1 = 0
    h1 = 0
    root.update()
    
    

    
def on_message2(client, userdata, msg2): #c
    global mess_3_timestamp
    t2 = 0
    h2 = 0
    dbflag = timeflag()
    timest = timestamp()
    t2, h2 = [float(x) for x in msg2.payload.decode("utf-8").split(',')]

    if dbflag - mess_3_timestamp > 3600:
        esp3(t2, h2, timest)
        mess_3_timestamp = timeflag()
    timest = str(timest)
    t2 = str(t2) # tkinter requires the str value
    h2 = str(h2)
    label_3 = Label(root, text= timest + " temperature in kitchen is " + t2 + "  humidity is " + h2, font=("helvetica", 25), fg="white", bg="black")
    label_3.grid(row=6, column=1)
    t2 = 0
    h2 = 0
    root.update()
    

    
    
def on_message3(client, userdata, msg3): #c
    global mess_4_timestamp
    t3 = 0
    h3 = 0
    dbflag = timeflag()
    t3, h3 = [float(x) for x in msg3.payload.decode("utf-8").split(',')]
    
    timest = timestamp()
    if dbflag - mess_4_timestamp > 3600:
        esp4(t3, h3, timest)
        avg_display() # here we call the average function when hedgehogs room temp hum and rounds are searching from database
        mess_4_timestamp = timeflag()
    timest = str(timest)
    t3 = str(t3) # tkinter requires the str value
    h3 = str(h3)
    label_4 = Label(root, text= timest + " temperature in outside kitchen is " + t3 + " humidity is " + h3, font=("helvetica", 25), fg="white", bg="black")
    label_4.grid(row=8, column=1)
    t3 = 0
    h3 = 0
    root.update()
    
    
def on_message4(client, userdata, msg9): #c
    global mess_5_timestamp
    t6 = 0
    h6 = 0
    dbflag = timeflag()
    t6, h6 = [float(x) for x in msg9.payload.decode("utf-8").split(',')]
    
    timest = timestamp()
    #if dbflag - mess_4_timestamp > 3600: # remember to add database on this function call.
    #    esp4(t3, h3, timest)
    #    avg_display() # here we call the average function when hedgehogs room temp hum and rounds are searching from database
    #    mess_4_timestamp = timeflag()
    timest = str(timest)
    t6 = str(t6) # tkinter requires the str value
    h6 = str(h6)
    label_4 = Label(root, text= timest + " temperature in bedroom is " + t6 + " humidity is " + h6, font=("helvetica", 27), fg="white", bg="black") # remember row
    label_4.grid(row=10, column=1)
    t3 = 0
    h3 = 0
    root.update()
    

    
    
    

def avg_display():
    global avg0, avg1, avg3, avg4
    hedge_temp_avg, hedge_temp  = hedge_room_temp()#here we get to database and search hedgehogs room temperature from database
    hedge_temp_avg = hedge_temp_avg[-1] # and average
    avg0, avg1 = average() # temperature averages
    avg3, avg4 = average_k()
    try:
        hedge_temp = hedge_temp[0] # if search result is empty i make this try except clause
        hedge_hum = hedge_temp[1]
    except IndexError:
        hedge_temp = 0 # if database search is empy then we printout zero
        hedge_hum = 0
    avg0 = avg0[-1]
    avg1 = avg1[-1]
    avg3 = avg3[-1]
    avg4 = avg4[-1]
    avg0 = str(avg0[0]) # tkinter requires the str value
    avg1 = str(avg1[0])
    avg3 = str(avg3[0])
    avg4 = str(avg4[0])
    hedge_temp_avg = str(hedge_temp_avg[0])
    hedge_temp = str(hedge_temp[0])
    hedge_hum = str(hedge_hum)
    label_5 = Label(root, text= " average per week living room is " + avg0 + "c." + " and outside " + avg1 + "c." ,  font=("helvetica", 25), fg="white", bg="black")
    label_5.grid(row=16, column=1, )
    label_6 = Label(root, text= " average per week kitchen is " + avg3  + "c." + " and outside " + avg4 + "c.",  font=("helvetica", 25), fg="white", bg="black")
    label_6.grid(row=18, column=1)
    root.update()
    run = hedge_24h()
    #print(run[0])
    day_run = 0
    total = sum(t[0] for t in run)
    print(total)
    total1 = total * 1.14
    total1 = '{:.2f}'.format(total1)
    total = str(total)
    total1 = str(total1)
    label_12 = Label(root, text= "hedgehogs run from 24 hours is: " + total + " rounds, and in meters : " + total1,  font=("helvetica", 25), fg="white", bg="black")
    label_12.grid(row=12, column=1)
    label_13 = Label(root, text= "hedgehogs room temp avarage per week: " + hedge_temp_avg + " and temp + humidity now is: " + hedge_temp +"c " + hedge_hum +"%" ,  font=("helvetica", 25), fg="white", bg="black")
    label_13.grid(row=14, column=1)
    root.update()
    


def ask_forecast():
    global image1
    global power_on
    Forecast = {}
    Forecast = fore_cast() #here we call the forecast.py function and this function returns a list where i digout the data
    #print(Forecast)
    #x = slice(0, 1, 2)
    Forecasttemp = Forecast[1]
    Forecasttimest = Forecast[2]
    Forecasttemp = str(Forecasttemp)
    Forecasttimest = str(Forecasttimest)
    Forecasttemp1 = Forecast[4]
    Forecasttimest1 = Forecast[5]
    Forecasttemp1 = str(Forecasttemp1)
    Forecasttimest1 = str(Forecasttimest1)
    Forecasttemp2 = Forecast[7]
    Forecasttimest2 = Forecast[8]
    Forecasttemp2 = str(Forecasttemp2)
    Forecasttimest2 = str(Forecasttimest2)
    Forecasttemp3 = Forecast[10]
    Forecasttimest3 = Forecast[11]
    Forecasttemp3 = str(Forecasttemp3)
    Forecasttimest3 = str(Forecasttimest3)
    Forecasttemp4 = Forecast[13]
    Forecasttimest4 = Forecast[14]
    Forecasttemp4 = str(Forecasttemp4)
    Forecasttimest4 = str(Forecasttimest4)
    img5=weathericon(Forecast[0]) # here we get the right image what is in desscription
    img4=weathericon(Forecast[3])
    img3=weathericon(Forecast[6])
    img2=weathericon(Forecast[9])
    img1=weathericon(Forecast[12])
    #print(Forecast[x])
    label_7 = Label(root, text= "next 5 day forecast is: " + Forecast[0] + " " + Forecasttemp + "c. Time: " + Forecasttimest  ,  font=("helvetica", 20), fg="white", bg="black")
    label_7.grid(row=20, column=1, )
    imagebutton = Button(root, image=img5) # this button was only way to add image on text line, iam not sure is there better way to do this
    imagebutton.grid(row=20, column=0, pady=0, padx=0, ipadx=0)
    label_8 = Label(root, text= Forecast[3] + " " + Forecasttemp1 + "c. Time: " + Forecasttimest1 ,  font=("helvetica", 20), fg="white", bg="black")
    label_8.grid(row=22, column=1)
    imagebutton1 = Button(root, image=img4)
    imagebutton1.grid(row=22, column=0, pady=0, padx=0, ipadx=0)
    label_9 = Label(root, text= Forecast[6]  + " " + Forecasttemp2 + "c. Time: " + Forecasttimest2   ,  font=("helvetica", 20), fg="white", bg="black")
    label_9.grid(row=24, column=1)
    imagebutton2 = Button(root, image=img3)
    imagebutton2.grid(row=24, column=0, pady=0, padx=0, ipadx=0)
    label_10 = Label(root, text= Forecast[9]+ " " + Forecasttemp3 + "c. Time: " + Forecasttimest3  ,  font=("helvetica", 20), fg="white", bg="black")
    label_10.grid(row=26, column=1)
    imagebutton3 = Button(root, image=img2)
    imagebutton3.grid(row=26, column=0, pady=0, padx=0, ipadx=0)
    label_11 = Label(root, text= Forecast[12]+ " " + Forecasttemp4 + "c. Time: " + Forecasttimest4 ,  font=("helvetica", 20), fg="white", bg="black")
    label_11.grid(row=28, column=1)
    imagebutton4 = Button(root, image=img1)
    imagebutton4.grid(row=28, column=0, pady=0, padx=0, ipadx=0)
    
    root.update()
    if power_on == 1: #here we power on the esp boards and hedgehogs counter
        plug_on()
        power_on = 0

def weathericon(Forecast): # here we compare the description and choose right image. there was lots of descriptions so i leave there else klause
    global image1
    global image2
    global image3
    global image4
    global image5
    global image6
    global image7
    global image8
    global image9
    if Forecast == "Overcast clouds": # pilvisä:
        imgpw = image3
        return imgpw
    if Forecast == "Few clouds" or Forecast == "Broken clouds" or Forecast == "Scattered clouds":  # vähän pilvistä
        imgpw = image7
        return imgpw
    if Forecast == "Light snow" or Forecast == "Snow" or Forecast == "Heavy Snow" or Forecast == "Mix snow/rain" or Forecast == "Snow shower" : #lunta
        imgpw = image5
        return imgpw
    if Forecast == "Clear sky":
        imgpw = image2
        return imgpw
    if Forecast == "Fog" or Forecast == "Freezing Fog" or Forecast == "Haze" or Forecast == "Smoke" or Forecast == "Mist": # sumua
        imgpw = image9
        return imgpw
    if Forecast == "Thunderstorm with light rain" or Forecast == "Thunderstorm with rain" or Forecast == "Thunderstorm with heavy rain": #ukkoskuuroja
        imgpw = image6
        return imgpw
    if Forecast == "Thunderstorm with light drizzle" or Forecast == "Thunderstorm with drizzle" or Forecast == "Thunderstorm with heavy drizzle" or Forecast == "Thunderstorm with Hail": # ukkosta
        imgpw = image8
        return imgpw
    if Forecast == "Light Drizzle" or Forecast == "Drizzle" or Forecast == "Heavy Drizzle" or Forecast == "Light Rain" or Forecast == "Moderate Rain" or Forecast == "Heavy Rain" or Forecast == "Freezing rain" or Forecast == "Light shower rain" or Forecast == "Shower rain" or Forecast == "Heavy shower rain":
        imgpw = image1 #sateet
        return imgpw
    else:
        imgpw = image4
        return imgpw
    
 
def shutdownmachine(inputpin):
    global inp
    inp = GPIO.input(26)
    if inp == 1:
        print("perkele")
        plug_off() # here we shutdown the remote plugs and hedgehogs counter from shutdown.py
    
    
root = Tk()
root.title('weather station')
root.geometry("1900x1080")
root.configure(background="black")

  
inputpin = 26
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(inputpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(inputpin, GPIO.FALLING, callback=shutdownmachine) # if shutdown pressed, we go to function shutdownmachine
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
inp = GPIO.input(26)

# here is tkinter setup

image1 = Image.open('/home/pi/Desktop/new/new_weatherstation/main_device/drizzle1.png') # rain
image1 = ImageTk.PhotoImage(image1, size= -5000)
image2 = Image.open('/home/pi/Desktop/new/new_weatherstation/main_device/clear.png') # sunny
image2 = ImageTk.PhotoImage(image2, size= -5000)
image3 = Image.open('/home/pi/Desktop/new/new_weatherstation/main_device/cloud.png') # clouds
image3 = ImageTk.PhotoImage(image3, size= -5000)
image4 = Image.open('/home/pi/Desktop/new/new_weatherstation/main_device/overcast.png') # clouds
image4 = ImageTk.PhotoImage(image4, size= -5000)
image5 = Image.open('/home/pi/Desktop/new/new_weatherstation/main_device/snow.png') # snowing
image5 = ImageTk.PhotoImage(image5, size= -5000)
image6 = Image.open('/home/pi/Desktop/new/new_weatherstation/main_device/sun_thunder.png') # thunder and sun
image6 = ImageTk.PhotoImage(image6, size= -5000)
image7 = Image.open('/home/pi/Desktop/new/new_weatherstation/main_device/weather_few_clouds.png') # few clouds
image7 = ImageTk.PhotoImage(image7, size= -5000)
image8 = Image.open('/home/pi/Desktop/new/new_weatherstation/main_device/weather_storm.png') # thunderdstorm
image8 = ImageTk.PhotoImage(image8, size= -5000)
image9 = Image.open('/home/pi/Desktop/new/new_weatherstation/main_device/foggy.png') # foggy
image9 = ImageTk.PhotoImage(image9, size= -5000)
btn = Button(root, text="view history",fg="white", bg="black",font=("helvetica", 15), command=lambda: history()).grid(row=30, column=1, pady=0, padx=0, ipadx=0) # put this to weatherstation
btn6 = Button(root, text="update the forecast view here",fg="white", bg="black",font=("helvetica", 15), command= ask_forecast).grid(row=32, column=1, pady=0, padx=0, ipadx=0)
btn7 = Button(root, text="update the database to web server",fg="white", bg="black",font=("helvetica", 15), command= lambda: history()).grid(row=34, column=1, pady=0, padx=0, ipadx=0)
btn8 = Button(root, text="restart esp boards",fg="white", bg="black",font=("helvetica", 15), command= lambda: reset_esp_boards()).grid(row=36, column=1, pady=0, padx=0, ipadx=0)

root.update()
ask_forecast()
avg_display()

# here is mqtt broker setup. here is also this message_callback_add what saves my project.
client = mqtt.Client()
client.on_connect = on_connect
client.message_callback_add('temp_humidity', on_message)
client.message_callback_add('temp_humidity1', on_message1)
client.message_callback_add('temp_humidity2', on_message2)
client.message_callback_add('temp_humidity3', on_message3)
client.message_callback_add('temp_humidity_bedroom', on_message4)
root.after(1000, lambda: root.update())
#client.on_connect = on_connect1# Specify on_connect callback
client.on_message = on_message # Specify on_message callback 
client.connect('localhost', 1883, 60)# Connect to MQTT broker (also running on Pi).   
client.loop_forever() #  Processes MQTT network traffic, callbacks and reconnections. (Blocking)

    