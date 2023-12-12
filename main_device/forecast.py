import requests
import credentials
import re
import json
import requests
from passwd import *
import pprint

api = forecast_api()
url = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/3hourly"

querystring = {"lat":"61.49","lon":"23.78","units":"metric"} # here is locatuion setup

headers = {
    'x-rapidapi-key': api,
    'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)


def fore_cast():
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    # here we digout from json format right information
    day1d = data['data'][-1]['weather']['description']
    #print(day1d)
    day1t = data['data'][-1]['temp']
    #print(day1t)
    day1time = data['data'][-1]['timestamp_local']
    day1Icon = data['data'][-1]['weather']['icon']
    #print(day1time)
    day2d = data['data'][-9]['weather']['description']
    #print(day2d)
    day2t = data['data'][-9]['temp']
    #print(day2t)
    day2time = data['data'][-9]['timestamp_local']
    day2Icon = data['data'][-9]['weather']['icon']
    #print(day2time)
    day3d = data['data'][-18]['weather']['description']
    #print(day3d)
    day3t = data['data'][-18]['temp']
    #print(day3t)
    day3time = data['data'][-18]['timestamp_local']
    day3Icon = data['data'][-18]['weather']['icon']
    #print(day3time)
    day4d = data['data'][-24]['weather']['description']
    #print(day4d)
    day4t = data['data'][-24]['temp']
    #print(day4t)
    day4time = data['data'][-24]['timestamp_local']
    day4Icon = data['data'][-24]['weather']['icon']
    #print(day4time)
    day5d = data['data'][-32]['weather']['description']
    #print(day5d)
    day5t = data['data'][-32]['temp']
    #print(day5t)
    day5time = data['data'][-32]['timestamp_local']
    day5Icon = data['data'][-32]['weather']['icon']
    print(day1Icon,day2Icon,day3Icon,day4Icon,day5Icon)

    Forecast = [] # here we back the values to list and return it to weatherstation
    Forecast = day1d, day1t, day1time, day1Icon, day2d, day2t, day2time, day2Icon, day3d, day3t, day3time, day3Icon, day4d, day4t, day4time,day4Icon,  day5d, day5t, day5time, day5Icon
    #print("whole data", data)
    return Forecast

#answ = resp[0:2]
#print(response.text)
#pprint.pprint(response.json())

#print(response.json())
#fore = fore_cast()
#print(fore)