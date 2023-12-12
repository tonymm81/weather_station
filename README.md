# weatherstation
this is a weatherstation where is connected three esp32 boards to raspberry pi3 and one raspberry pi2 is connected also. each esp boards has 1 dht11 and dht22 sensors 
except bedroom device and rasbperrypi 2 has one.

rasbperrypi2 is a hedgehogs spinning wheel calculator what updates the temperatures and spinning records per hour

esp softwares are in own folders. esp:kitchen etc..

and hedgehogs spinning wheel calculator is own folder called calculator

and main device files are in main device. this device is keeping the database up and updates the values inside it. it also is a mqtt broker.
main device has tkinter window where it show information. it updates this 4 dht11 sensors from espboards to screen and once per hour
it updates the temp and hum to database. it calculates the average value from temp in 4 sensors and rasbperrypi 2 dht sensor also.
it have program called hedgehogmqtt.py what listens if the raspberrypi2 sends a temps or results of spinning wheel.

this maindevice also takes a week forecast from api service.

raspberry pi2 is a counter what keeps writing records to logfile, and thingspeak api service and in main device database. 
this device has magnetic pulse sensors in spinning wheel and small piece of iron. when sensor activates it takes rasbperri pi 2 gpio pin up.
then the program calculated 1 round. there is also timestamps inside of this laskuriapi.py file. i make a module what sends data to main device.
file name is hedgehog.py. laskuriapi calls it when time condition is true:

i put the comments to code so perhaps it explain how this works. there is also plan.txt where you can see the plans and bugs and reports etc.

here is the files what i code:
main device: 
weatherstation.py
hedgehogmqtt.py
database.py
forecast.py
search_database.py
shutdown.py
graphics.py
broadlink_switch.py
scroll.py
connections.py

and esp boards
boot.py 

in hedgehogs spinning wheel calculator
laskuriapi.py
hedgehog.py

sort describe: weatherstation.py keeps graphics up and update the sensor measurements to screen.  this main program calls also 
forecast.py where we get a 5 day forecast.

hedgehogmqtt.py listens to connection from raspberrypi2 calculator. when it sends a message this program upload the recieved data to database.

database.py is handling the database and programs are calling it when the time rule is true.

forecast.py i e here free api service where i get this information. this forecasti is calling only then when program is starting.

boot.py is file what is inside the esp32 boards. this measure the sensor data and send it to broker(main device)

laskuriapi.py is calculating the wheel rounds with gpio pin from raspberry pi 2. this program keeps a log file and every hour it start from 0 and keep the old measurements.
this program also upload the data to thingview and also upload the data to main device with mqtt.

hedgehog.py is the program what is mqtt client. when time rule is true it upload the spinning wheel rounds and temperature and humidity to main device.

scroll.py is the view where we printout the database data what user want to search

dbsearch.py is popup window application what we call from weatherstation. there user choice what device data history she/he want to search

shutdown.py starts and resets and shutdown the esp boards.

broadlink_switch.py is controlling the wlan plugs. or reseting them.

search_database.py is the db_search.py connected file. here is the database search codes.

graphics.py is drawing the blocks on choosen measurements.

connections.py is keeping the mqtt connection up where esb boards are sendind the measurement values.
it communicates with weatherstation.py with pickle messages.

weatherstation.py keeps up the graphics and also controlling the wlan plugs if some of esp boards is offline

scroll.py is the graphical view, where user can choose what device measurements is showing on grapgics.py

updated large changes on version 134. I clean out the code really much.
The database table is now only one table so easier to use calendar view examble.

More specific information about versions in plans.txt