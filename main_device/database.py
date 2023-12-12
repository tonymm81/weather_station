import mariadb
import sys
from scroll import *
from passwd import *

    
def hedgehog1(hedge_run, timest): # here we upload the hedgehogs runnings
    conn, cur = connect()
    cur.execute(
    "INSERT INTO siili (juoksut, timestamp) VALUES (%s, %s)", 
    (hedge_run, timest))
    conn.commit()
    # in this part i will build up the counting of last 24 hours
    conn.close()
    
    
    
def hedge_24h(): # here we calculated how much heedgehog has run per 24hours
    conn, cur = connect()
    cur.execute(
        "SELECT juoksut FROM siili WHERE timestamp > DATE_SUB(CURDATE(), INTERVAL 1 DAY)" 
    )
    run= cur.fetchall()
    conn.close
    return run

    
def average(): # livingroom average
    #avg = 0.0
    conn, cur = connect()  
    cur = conn.cursor()
    cur.execute(
    "SELECT CAST(AVG(temperature_living_in) as dec(10,2)) FROM all_sensors GROUP BY WEEK(time_id)",
    )
    #conn.commit()
    living_in_temp = cur.fetchall()

    cur.execute(
    "SELECT CAST(AVG(temperature_living_out) AS DEC(10,2)) FROM all_sensors GROUP BY WEEK(time_id)" 
    )
    living_out_temp = cur.fetchall()
    cur.execute(
    "SELECT CAST(AVG(temperature_kitchen_in) AS DEC(10,2)) FROM all_sensors GROUP BY WEEK(time_id)" 
    )
    #conn.commit()
    kitchen_in_temp = cur.fetchall()
    #avg3 = round(avg3, 2)
    
    cur.execute(
    "SELECT CAST(AVG(temperature_kitchen_out) AS DEC(10,2)) FROM all_sensors GROUP BY WEEK(time_id)" 
    )
    kitchen_out_temp = cur.fetchall()

    conn.close()
    
    return living_in_temp, living_out_temp, kitchen_in_temp, kitchen_out_temp



def save_sensors_value(esp_json_message): # this is updated in version 133
    print("oujea")
    conn, cur = connect()   
    cur = conn.cursor()
    query = "INSERT INTO all_sensors(time_id, temperature_living_in, humidity_living_in, temperature_living_out, humidity_living_out, lux_value_livingroom, temperature_kitchen_in, humidity_kitchen_in, temperature_kitchen_out, humidity_kitchen_out, lux_value_kitchen, bedroom_temperature, bedroom_humidity) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"
    values = [esp_json_message['livingroom_timestamp'], 
              esp_json_message['livingroom_indoor_temp'],
              esp_json_message["livingroom_indoor_humidity"],
              esp_json_message["livingroom_outside_temp"],
              esp_json_message["livingroom_outside_humidity"],
              esp_json_message["lux_value_livingroom"],
              esp_json_message["kitchen_indoor_temp"],
              esp_json_message["kitchen_indoor_humidity"],
              esp_json_message["kitchen_outdoor_temp"],
              esp_json_message["kitchen_outdoor_humidity"],
              esp_json_message["lux_value_kitchen"],
              esp_json_message["bedroom_temp"],
              esp_json_message["bedroom_humidity"]]
    cur.execute(query, values)
    conn.commit()
    conn.close()
    values = []


def connect(): # here is database connections
    import mariadb 
    import sys
    #connect()
    user, passwd = dbpass()
    conn = mariadb.connect(
        user=user,
        password=passwd,
        host="localhost",
        port=3306,
        database="weatherstation"
        )

    cur = conn.cursor()
    return conn, cur