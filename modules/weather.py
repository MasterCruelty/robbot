import sys
sys.path.append(sys.path[0] + "/..")
from modules.gmaps import showmaps
import requests
import json
from datetime import date,datetime as dt
import pytz
from utils.get_config import *
from pyrogram import Client,filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from pyrogram.handlers import CallbackQueryHandler

config_file = get_config_file("../config.json")
api_weather = config_file["api_weather"]


#dizionario per i codici di visualizzazione delle mappe satellitari
sat24_codes = {"pioggia"    : "rainTMC",
               "sole"       : "visual",
               "infrarossi" : "infraPolair",
               "neve"       : "snow"
              }
"""
    Funzione di supporto che chiama le api di OpenWeatherMap(Dati principali meteo)
"""
def call_api_weather(query):
    coordinates = showmaps(query,"client","message") #showmaps will raise an exception and return only coordinates
    if("404:" in str(coordinates)):
        return coordinates
    lat = coordinates[0]
    lon = coordinates[1]
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&lang=it&appid=%s&units=metric" %(lat,lon,api_weather)
    response = requests.get(url)
    data = json.loads(response.text)
    return data

"""
    Funzione di supporto che chiama le api di OpenWeatherMap (dati sulla qualità dell'aria)
"""
def call_api_airPollution(query):
    coordinates = showmaps(query,"client","message") #showmaps will raise an exception and return only coordinates
    lat = coordinates[0]
    lon = coordinates[1]
    url = "https://api.openweathermap.org/data/2.5/air_pollution?lat=%s&lon=%s&lang=it&appid=%s&units=metric" %(lat,lon,api_weather)
    response = requests.get(url)
    data = json.loads(response.text)
    return data

"""
    Funzione di supporto che converte il codice della qualità dell'aria al suo valore letterale associato
"""
def check_airQualityCode(air_quality):
    if air_quality == 1:
        return "Ottima"
    if air_quality == 2:
        return "Buona"
    if air_quality == 3:
        return "Accettabile"
    if air_quality == 4:
        return "Bassa"
    if air_quality == 5:
        return "Molto bassa"


"""
    Dato il nome di una città, viene usata la funzione "showmaps" del modulo gmaps per ricavarne le coordinate. Dopo di che viene fatta la richiesta diretta a 
    OpenWeatherMap tramite la funzione "call_api_weather" rilasciando i dati meteo principali relativi al giorno corrente.
"""
def get_weather(query,client,message):
    try:
        data = call_api_weather(query)
    except AttributeError:
        return sendMessage(client,message,"__404: not found__")
    if("404:" in str(data)):
        return sendMessage(client,message,data)
    data_air = call_api_airPollution(query)
    current_temp = str(data["current"]["temp"])
    feels_temp = str(data["current"]["feels_like"])
    umidita = str(data["current"]["humidity"]) # % of umidity
    clouds = str(data["current"]["clouds"])    # % of cloudiness
    visibility = str(data["current"]["visibility"]) # Visibility in metres
    wind_speed = data["current"]["wind_speed"] * 3.6 #speed in m/s
    wind_speed = str(round(wind_speed,2))
    weather = data["current"]["weather"][0]["description"]
    #sunrise and sunset UNIX time
    sunset = data["current"]["sunset"]
    sunrise = data["current"]["sunrise"]
    #Conversion to Europe/Rome timezone
    sunset = str(dt.fromtimestamp(sunset, pytz.timezone('Europe/Rome')))[10:]
    sunrise = str(dt.fromtimestamp(sunrise, pytz.timezone('Europe/Rome')))[10:]
    #air pollution data
    air_qualityCode = data_air["list"][0]["main"]["aqi"]
    air_quality = check_airQualityCode(air_qualityCode) #convert air code to the real meaning
    pm10 = str(data_air["list"][0]["components"]["pm10"]) + " μg/m3  [Limite soglia giornaliera = 50 μg/m3]"
    pm25 = str(data_air["list"][0]["components"]["pm2_5"]) + " μg/m3  [Limite annuo = 25 μg/m3]"
    #Result string
    result = "**" + query.title() + "**" + "\n**Meteo:** __" + weather + "__\n**Temperatura attuale:** __" + current_temp + " C°__.\n**Temperatura percepita:** __" + feels_temp + " C°__.\n**Umidità:** __" + umidita + "%__.\n**Nuvole:** __" + clouds + "%__.\n**Visibilità:** __" + visibility + " metri__.\n**Velocità del vento:** __" + wind_speed + " km/h__.\n**Ora alba:** __" + sunrise + "__\n**Ora tramonto:** __" + sunset + "__\n\n**Qualità dell'aria:** __" + air_quality + "__\n**PM10:** __" + pm10 + "__\n**PM2.5:** __" + pm25 + "__"
    return sendMessage(client,message,result)


"""
    Json ottenuto in modo analogo a "get_weather" e vengono rilasciati i dati meteo principali del giorno corrente distanziati di ora in ora.
"""
global pages_t #usata per popolare la lista che si andrà a scorrere tramite i bottoni inline
global k1 #indice globale per gestire gli elementi di pages da restituire premendo il bottone inline

@Client.on_message()
def get_today_forecasts(query,client,message):
    global pages_t
    global k1
    data = call_api_weather(query)
    array_hourly = data["hourly"]
    today = date.today()
    today = str(today.strftime("%Y-%m-%d"))
    result = "**" + query.title() + "** __" + str(today) + "__\n\n"
    pages_t = []
    z = 0 #variabile ausiliaria locale per popolare pages
    

    #Costruisco la stringa formattata e popolo la globale pages 
    for item in array_hourly:
        giorno = str(dt.fromtimestamp(item["dt"],pytz.timezone('Europe/Rome')))
        if(giorno[0:10] != today):
            break
        giorno = giorno[10:]
        temp = str(item["temp"]) + " C°"
        feels_temp = str(item["feels_like"]) + " C°"
        clouds = str(item["clouds"]) + "%"
        weather = item["weather"][0]["description"]
        result += giorno + "\n**Meteo:** __" + weather + "__\n**Temperatura:** __" + temp + "__\n**Temperatura percepita:** __" + feels_temp + "__\n**Nuvole:** __" + clouds + "__\n##################\n\n" 
        z = z + 1
        if(z % 2 == 0):
            pages_t.append(result)
            result = "**" + query.title() + "** __" + str(today) + "__\n\n"
        elif("23" in giorno):
            pages_t.append(result)
            result = "**" + query.title() + "** __" + str(today) + "__\n\n"


    
    #Tiro su la tastiera e aggiungo l'handler
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("Prossima fascia oraria",callback_data="forecastoday")]])
    client.add_handler(CallbackQueryHandler(callback=press_forecastoday,filters= filters.regex("forecastoday")))
    k1 = 0
    client.send_message(get_chat(message),pages_t[k1],reply_markup=kb,reply_to_message_id=get_id_msg(message))

"""
    Funzione che viene chiamata quando è premuto il bottone associato alla funzione get_today_forecasts.
    A ogni pressione si scorrono le pagine ovvero gli elementi contenuti nella variabile globale pages.
"""
@Client.on_callback_query(filters = filters.regex("forecastoday"))
def press_forecastoday(client,message):
    print("Giro pagina in /forecastoday")
    global k1
    if k1 < len(pages_t)-1:
        k1 = k1 + 1
        kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("Prossima fascia oraria",callback_data="forecastoday")]])
        message.edit_message_text(pages_t[k1],reply_markup=kb)
    else:
        message.edit_message_text("__Fine__")


"""
    Json ottenuto in modo analogo a "get_weather" e vengono rilasciati i dati meteo principali della settimana che verrà.
"""
global pages_f
global k2
@Client.on_message()
def get_future_forecasts(query,client,message):
    global pages_f
    global k2
    data = call_api_weather(query)
    array_daily = data["daily"]
    result = "**" + query.title() + "**\n\n"
    pages_f = []
    for item in array_daily:
        giorno = str(dt.fromtimestamp(item["dt"],pytz.timezone('Europe/Rome')))[0:10]
        sunset = str(dt.fromtimestamp(item["sunset"], pytz.timezone('Europe/Rome')))[10:]
        sunrise = str(dt.fromtimestamp(item["sunrise"], pytz.timezone('Europe/Rome')))[10:]
        morning = str(item["temp"]["morn"]) + " C°"
        day = str(item["temp"]["day"]) + " C°"
        evening = str(item["temp"]["eve"]) + " C°"
        night = str(item["temp"]["night"]) + " C°"
        feels_morning = str(item["feels_like"]["morn"]) + " C°"
        feels_day = str(item["feels_like"]["day"]) + " C°"
        feels_evening = str(item["feels_like"]["eve"]) + " C°"
        feels_night = str(item["feels_like"]["night"]) + " C°"
        temp_min = str(item["temp"]["min"])+ " C°"
        temp_max = str(item["temp"]["max"])+ " C°"
        umidita = str(item["humidity"]) + "%" # % of umidity
        wind_speed = item["wind_speed"] * 3.6 #speed in m/s
        wind_speed = str(round(wind_speed,2))
        clouds = str(item["clouds"]) + "%"
        weather = item["weather"][0]["description"]
        result += "**__" + giorno + "**__\n**Meteo:** __" + weather + "__\n**Temperatura reale/percepita\n\nMattina:** __" + morning + " / " + feels_morning + "__\n**Giorno:** __" + day + " / " + feels_day + "__\n**Sera:** __" +  evening + " / " + feels_evening + "\n**Notte:** __" + night + " / " + feels_night + "\n**Minima:** __" + temp_min + "__\n**Massima:** __" + temp_max + "__\n**Umidità:** __" + umidita + "__\n**Velocità del vento:** __" + wind_speed + " km/h__\n**Nuvole:** __" + clouds + "__\n--**#################**--\n\n"
        pages_f.append(result)
        result = "**" + query.title() + "**\n\n"
    

    #Tiro su la tastiera e aggiungo l'handler
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("Prossimo giorno",callback_data="forecastFuture")]])
    client.add_handler(CallbackQueryHandler(callback=press_forecastfuture,filters=filters.regex("forecastFuture")))
    k2 = 0
    client.send_message(get_chat(message),pages_f[k2],reply_markup=kb,reply_to_message_id=get_id_msg(message))


"""
    Funzione che viene chiamata quando è premuto il bottone associato alla funzione get_future_forecasts.
    A ogni pressione si scorrono le pagine ovvero gli elementi contenuti nella variabile globale pages.
"""
@Client.on_callback_query(filters = filters.regex("forecastFuture"))
def press_forecastfuture(client,message):
    print("Giro pagine in /forecastfuture")
    global k2
    if k2 < len(pages_f)-1:
        k2 = k2 + 1
        kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("Prossimo giorno",callback_data="forecastFuture")]])
        message.edit_message_text(pages_f[k2],reply_markup=kb)
    else:
        message.edit_message_text("__Fine__")

    

"""
Data una richiesta, restituisce l'immagine della mappa corrispondente con il meteo attuale offerto da wttr.in
"""
def wttrin_map(query,client,message):
    img = "https://v3.wttr.in/" + query + ".png"
    try:
        return sendPhoto(client,message,img,caption="__Area **"+query+"** come richiesto.__")
    except:
        return sendMessage(client,message,"__404: page not found__")

"""
Data una richiesta, restituisce l'immagine gif satellitare dell'area.
"""
def sat24_map(query,client,message):
    query = query.split(",")
    try:
        area = query[0]
        code = query[1].replace(" ","")
        img = "https://api.sat24.com/animated/"+ area + "/"+ sat24_codes[code] + "/2/Central%20European%20Standard%20Time/6030397'%20width=400%20height=291"
        return sendGIF(client,message,img,caption="__Ecco la mappa satellitare richiesta.__")
    except:
        return sendMessage(client,message,"__Mappa non trovata o richiesta errata.\nConsulta **/helprob meteo** per più informazioni.__")
