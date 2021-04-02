from geopy.geocoders import Nominatim
from geopy.distance  import geodesic
from pyrogram import Client
import time
import json
import sys
sys.path.append(sys.path[0] + "/..")
from utils.get_config import *


def execute_km(query,client,message):
    addresses = query.split(',')
    km = distanza(addresses[0],addresses[1])
    result = "La distanza tra i due luoghi è di " + str(km) + " km."
    return sendMessage(client,message,result)

@Client.on_message()
def showmaps(address,client,message):
    geolocate = Nominatim(user_agent="Robbot")
    location  = geolocate.geocode(address,timeout=10000)
    coordinates = []
    try:
        coordinates.append(location.latitude)
        coordinates.append(location.longitude)
    except:
        return sendMessage(client,message,"__Error 404: not found__")
    try:
        client.send_location(get_chat(message),coordinates[0],coordinates[1],reply_to_message_id=get_id_msg(message))
    except:
        return coordinates

def distanza(address1,address2):
    coord1 = showmaps(address1,client = None,message = None)
    coord2 = showmaps(address2,client = None,message = None)
    departure = (coord1[0],coord1[1])
    arrive = (coord2[0],coord2[1])
    result = geodesic(departure,arrive).miles
    result = (result * 1.609344)
    return round(result,2)
