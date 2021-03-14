from gmaps import showmaps
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
    current_temp = data["current"]["temp"]
    feels_temp = data["current"]["feels_like"]
    umidita = data["current"]["humidity"] # % of umidity
    clouds = data["current"]["clouds"]    # % of cloudiness
    visibility = data["current"]["visibility"] # Visibility in metres
    wind_speed = data["current"]["wind_speed"] #speed in m/s
    weather = data["current"]["weather"][0]["description"]
    #sunrise and sunset UNIX time
    sunset = data["current"]["sunset"]
    sunrise = data["current"]["sunrise"]
    sunset = dt.fromtimestamp(sunset, pytz.timezone('Europe/Rome'))
    sunrise = dt.fromtimestamp(sunrise, pytz.timezone('Europe/Rome'))
