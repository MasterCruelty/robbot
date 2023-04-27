from geopy.geocoders import Nominatim
from geopy.distance  import geodesic
from pyrogram import Client
import json
import sys
sys.path.append(sys.path[0] + "/..")
from utils.get_config import *


not_found = "__Error 404: not found__"

"""
    query => le due località su cui calcolare la distanza con la virgola come separatore.
    client, message => dati per comunicare con pyrogram in sendMessage.

    Funzione che formatta l'input, esegue la funzione per calcolare la distanza tra i due luoghi e restituisce il risultato tramite messaggio.
"""
def execute_km(query,client,message):
    addresses = query.split(',')
    km = distanza(addresses[0],addresses[1])
    if(km == "None"):
        result = not_found
    else:
        result = "La distanza tra i due luoghi è di " + str(km) + " km."
    try:
        return sendMessage(client,message,result)
    except AttributeError:
        return km


"""
    address => indirizzo di cui si vuole sapere la localizzazione.
    client, message => dati per comunicare con pyrogram in send_location.

    Funzione che dato un indirizzo restituisce tramite messaggio la posizione geografica tramite le API dirette di Telegram.
    Viene usata anche come funzione ausiliaria in 'distanza', in quel caso restituisce solo l'array con le due coppie di coordinate.
"""
@Client.on_message()
def showmaps(address,client,message):
    check = False
    if "-i" in address:
        check = True
        address = address.replace("-i","")
    geolocate = Nominatim(user_agent="Robbot")
    location  = geolocate.geocode(address,timeout=10000)
    if location == None:
        try:
            return sendMessage(client,message,not_found)
        except AttributeError:
            print("errore generico")
    coordinates = []
    caption = "__**" + location.address + "\n\nTipologia luogo: " + location.raw["type"] + "\n\nImportanza: " + str(round(location.raw["importance"],2)) + "**__"
    caption += "\n\n__Importanza è un valore compreso tra 0 e 1 circa, calcolato in base al rank del luogo negli articoli di Wikipedia.__\n"
    url = "https://www.openstreetmap.org/#map=16/{}/{}".format(location.latitude, location.longitude)
    caption += "<a href=" + url + ">Guarda su OpenStreetMap</a>"
    if check == True:
        return sendMessage(client,message,caption)
    try:
        coordinates.append(location.latitude)
        coordinates.append(location.longitude)
    except AttributeError:
        return sendMessage(client,message,not_found)
    try:
        client.send_location(get_chat(message),coordinates[0],coordinates[1],reply_to_message_id=get_id_msg(message))
        return sendMessage(client,message,caption)
    except:
        return coordinates

"""
    address1 => il primo luogo.
    address2 => il secondo luogo.

    Data una coppia di coordinate geografiche, viene calcolata la distanza in linea d'aria dei due luoghi in km.
"""
def distanza(address1,address2):
    try:
        coord1 = showmaps(address1,client = None,message = None)
        coord2 = showmaps(address2,client = None,message = None)
    except:
        return "None"
    departure = (coord1[0],coord1[1])
    arrive = (coord2[0],coord2[1])
    result = geodesic(departure,arrive).miles
    result = (result * 1.609344)
    return round(result,2)
