import mariadb
import sys
from passwd import *
import datetime as dt




def what_device(device): # lets check what device user want to search and make db tables and column to python list and retun it to choicev function
    if device == "livingroom":
        column = (["time_id" ,"temperature_living_in", "humidity_living_in", 
                    "temperature_living_out", "humidity_living_out", "lux_value_livingroom"]) 
        table = "all_sensors"
        return column, table
    
    if device == "kitchen":
        column = (["time_id","temperature_kitchen_in", "humidity_kitchen_in", 
                   "temperature_kitchen_out", "humidity_kitchen_out", "lux_value_kitchen"])
        table = "all_sensors"
        return column, table
    
    if device == "bedroom":
        column = ["time_id", "bedroom_temperature", "bedroom_humidity"]
        table = "all_sensors"
        return column, table
    
    if device == "hedgerun": # hedgeruns db search keywords didnt need to change
        column = ""
        table = ""
        return column, table
    
    
def choicev(device, choice, start_date = dt.datetime.now(), end_date = dt.datetime.now()): # here is db search options. # ver 132 calemdar update
    conn, cur = connect()   
    cur = conn.cursor()
    print("in choicev function",device, choice, start_date, end_date)
    start_date_ = start_date # ver 132 calemdar update
    end_date_ = end_date # ver 132 calemdar update
    column, table = what_device(device)
    if device == "kitchen" or device == "livingroom": # here we search kitchen or livingroom
        if choice == "veek":    
            cur.execute("SELECT "+column[0]+","+  column[1]+ ", " + column[2] +"," +column[3]+","+column[4]+","+column[5]+" FROM "+table+"  WHERE  " +column[0]+ " > DATE(NOW()) - INTERVAL 7 DAY ORDER BY "+column[0]+" DESC ") 
            veek = cur.fetchall()
            print(veek)
            conn.close()
            return  device, veek
        if choice == "month":
            cur.execute("SELECT "+column[0]+","+ column[1]+ ", " + column[2] +"," +column[3]+","+column[4]+","+column[5]+" FROM "+table+" WHERE " +column[0]+ " > DATE(NOW()) - INTERVAL 30 DAY ORDER BY "+column[0]+" DESC ")
            month = cur.fetchall()
            return device, month
        if choice == "custom": # ver 132 calemdar update
            print(start_date_, end_date_)
            cur.execute("SELECT "+column[0]+","+ column[1]+ ", " + column[2] +"," +column[3]+","+column[4]+","+column[5]+"  FROM "+table+" WHERE " +column[0]+ " BETWEEN "+ start_date_+ " AND "+ end_date_+" ORDER BY "+column[0]+" DESC")
            year = cur.fetchall()
            return device, year
        if choice == "max":
            cur.execute("SELECT "+column[0]+","+column[1]+", MAX( "+column[2]+"),"+column[3]+", MAX("+column[4]+")  FROM "+table+"")
            maxresult = cur.fetchall()
            conn.close()
            return device, maxresult
        if choice == "min":
            cur.execute("SELECT "+column[0]+","+column[1]+", MIN( "+column[2]+"), MIN("+column[3]+"), "+column[4]+" FROM "+table+"")
            minresult = cur.fetchall()
            conn.close()         
            return device, minresult
        
    if device == "bedroom": #here we search result from bedroom of hedgeroom
        if choice == "veek":
            cur.execute("SELECT "+column[0] + ","+ column[1] + ","+ column[2] + " FROM " +table+" WHERE "+column[0]+" > DATE(NOW()) - INTERVAL 7 DAY ORDER BY "+column[0]+" DESC") 
            veek = cur.fetchall()
            conn.close()
            return device, veek
        if choice == "month":
            cur.execute("SELECT "+column[0] + ","+ column[1] + ","+ column[2] + " FROM " +table+" WHERE "+column[0]+" > DATE(NOW()) - INTERVAL 30 DAY ORDER BY "+column[0]+" DESC") 
            month = cur.fetchall()
            conn.close()
            return device, month
        if choice == "custom":
            cur.execute("SELECT "+column[0] + ","+ column[1] + ","+ column[2] + " FROM " +table+" WHERE "+column[0]+ " BETWEEN "+ start_date_+ " AND "+ end_date_+" ORDER BY "+column[0]+" DESC" ) #ver132 update
            year = cur.fetchall()
            conn.close()
            return device, year
        if choice == "max":
            cur.execute("SELECT "+column[1]+", MAX(temp) FROM "+table+"")
            result_max = cur.fetchall()
            conn.close()
            
            return device, result_max
        if choice == "min":
            cur.execute("SELECT "+column[1]+", MIN(temp) FROM "+table+"")
            result_min = cur.fetchall()
            conn.close()
            return device, result_min   
    
        
    
        
    if device == "hedgerun": # here we search hedgehogs running history
        if choice == "veek":
            cur.execute("SELECT siili.juoksut, siili.timestamp FROM siili  WHERE siili.timestamp > DATE(NOW()) - INTERVAL 7 DAY ORDER BY siili.timestamp DESC")
            hedge_run = cur.fetchall()
            conn.close()
            return device, hedge_run
        if choice == "month":
            cur.execute("SELECT siili.juoksut, siili.timestamp FROM siili  WHERE siili.timestamp > DATE(NOW()) - INTERVAL 30 DAY ORDER BY siili.timestamp DESC")
            hedge_run_m = cur.fetchall()
            conn.close()
            return device, hedge_run_m
        if choice == "custom":
            cur.execute("SELECT siili.juoksut, siili.timestamp FROM siili  WHERE (siili.timestamp BETWEEN "+start_date_+ " AND "+end_date_+ ") DESC ") #ver132 update
            hedge_run_y = cur.fetchall()
            conn.close()
            
            return device, hedge_run_y
        if choice == "max":
            cur.execute("SELECT MAX(juoksut), MAX(run_timestamp) FROM siili")
            hedge_max = cur.fetchall()
            conn.close()
            print(hedge_max)
            return device, hedge_max
        if choice == "min":
            cur.execute("SELECT MIN(juoksut), MIN(run_timestamp) FROM siili")
            hedge_min = cur.fetchall()
            
            conn.close()
            return device, hedge_min


    


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

#somelist=choicev("livingroom", "custom", "'2023-2-13'", "'2023-2-15'")
#print(somelist)