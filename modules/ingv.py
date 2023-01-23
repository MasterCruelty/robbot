from utils.get_config import sendMessage,get_chat,get_id_msg,sendPhoto
from pyrogram import Client,filters,errors
import re
import requests
from bs4 import BeautifulSoup
from georss_ingv_centro_nazionale_terremoti_client import IngvCentroNazionaleTerremotiFeed as ingv
import modules.gmaps as gm


"""
    Restituisce dati sui terremoti nei dintorni del luogo desiderato da INGV
"""
def get_eq_data(query,client,message):
    splitted = query.split(",")
    query_place = splitted[0]
    coordinates = gm.showmaps(query_place,"client","message")
    lat = coordinates[0]
    lon = coordinates[1]
    try:
        radius = int(splitted[1])
    except IndexError:
        radius = 0
    feed = ingv((lat,lon),filter_radius=radius,filter_minimum_magnitude=1.0)
    status,entries = feed.update()
    print(status)
    print("trovate " + str(len(entries)) + " entries")
    result = ""
    text_message = ""
    if len(entries) > 0:
        for i in range(len(entries)):
            print(entries[i].region)
            if i > 5:
                break
            event_id = entries[i].event_id
            #WIP
            resp = requests.get("webservices.ingv.it/fdsnws/event/1/query?eventId=" + event_id)
            place = entries[i].region
            magnitude = entries[i].magnitude
            map_image = entries[i].image_url
            splitted = place.split(" ")
            km = gm.distanza(query_place,splitted[3])
            result += "**" + place + "**\nmagnitudo: __" + str(magnitude) + "__\nA " +str(km)+" km da " + query_place.title() + "__\n\n"
            if map_image != None:
                sendPhoto(client,message,map_image,result)
            else:
                text_message += result
                result = ""
        if text_message != "":
            return sendMessage(client,message,text_message)
    else:
        return sendMessage(client,message,"__Nessun dato trovato__")
