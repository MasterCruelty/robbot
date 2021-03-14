import sys
sys.path.append(sys.path[0] + "/..")
from modules.gmaps import showmaps
import requests
import json
from datetime import datetime as dt
import pytz
from utils.get_config import *
from pyrogram import Client

config_file = get_config_file("../config.json")
api_weather = config_file["api_weather"]


def get_weather(client,message,query):
    coordinates = showmaps(query,"client","message") #showmaps will raise an exception and return only coordinates
    lat = coordinates[0]
    lon = coordinates[1]
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" %(lat,lon,api_weather)
    response = requests.get(url)
    data = json.loads(response.text)
    current_temp = str(data["current"]["temp"])
    feels_temp = str(data["current"]["feels_like"])
    umidita = str(data["current"]["humidity"]) # % of umidity
    clouds = str(data["current"]["clouds"])    # % of cloudiness
    visibility = str(data["current"]["visibility"]) # Visibility in metres
    wind_speed = data["current"]["wind_speed"] #speed in m/s
    wind_speed = str(wind_speed * 3.6)
    weather = data["current"]["weather"][0]["description"]
    #sunrise and sunset UNIX time
    sunset = data["current"]["sunset"]
    sunrise = data["current"]["sunrise"]
    sunset = str(dt.fromtimestamp(sunset, pytz.timezone('Europe/Rome')))[10:]
    sunrise = str(dt.fromtimestamp(sunrise, pytz.timezone('Europe/Rome')))[10:]
    result = "**" + query.title() + "**" + "\n**Temperatura attuale:** __" + current_temp + " C°__.\n**Temperatura percepita:** __" + feels_temp + " C°__.\n**Umidità:**__" + umidita + "%__.\n**Nuvole:** __" + clouds + "%__.\n**Visibilità:** __" + visibility + " metri__.\n**Velocità del vento:** __" + wind_speed + " km/h__.\n**Ora alba:** __" + sunrise + "__\n**Ora tramonto:** __" + sunset + "__"
    return sendMessage(client,message,result)

