from utils.get_config import sendMessage,sendPhoto,get_config_file
from pyrogram import Client,errors
import requests
import json
import random


"""
    Restituisce una foto di un gatto utilizzando un api pubblica
"""
def get_cat(_,client,message):
    url = "https://api.thecatapi.com/v1/images/search"
    resp = requests.get(url)
    data = json.loads(resp.text)
    img = data[0]['url']
    return sendPhoto(client,message,img,"Ecco un bel gatto")

"""
    Restituisce una foto di un cane utilizzando un api pubblica
"""
def get_dog(_,client,message):
    url = "https://dog.ceo/api/breeds/image/random"
    resp = requests.get(url)
    data = json.loads(resp.text)
    img = data['message']
    return sendPhoto(client,message,img,"Ecco un bel cane")

"""
    Restituisce una foto di una volpe utilizzando un api pubblica
"""
def get_fox(_,client,message):
    url = "https://randomfox.ca/floof/"
    resp = requests.get(url)
    data = json.loads(resp.text)
    img = data['image']
    return sendPhoto(client,message,img,"Ecco una bella volpe")

"""
    Restituisce una foto di un coniglio utilizzando un api pubblica
"""
config = get_config_file("config.json")
access_key = config["unsplash_key"]
def get_rabbit(_,client,message):
    url = 'https://api.unsplash.com/photos/random'
    params = {
        'query': 'rabbit',   
        'client_id': access_key,
        'count': 1  
    }
    
    resp = requests.get(url,params=params)
    if resp.status_code == 200:
        data = resp.json()
        image_url = data[0]['urls']['regular']
    else:
        return sendMessage(client,message,"__Errore nella richiesta.\nEsaurite richieste giornaliere forse.__")
    return sendPhoto(client,message,image_url,"Ecco un bel coniglio")

"""
    Restituisce foto di volatili utilizzando un api pubblica
"""
def get_bird(_,client,message):
    url = 'https://api.unsplash.com/photos/random'
    params = {
        'query': 'bird',   
        'client_id': access_key,
        'count': 1  
    }

    resp = requests.get(url,params=params)
    if resp.status_code == 200:
        data = resp.json()
        image_url = data[0]['urls']['regular']
    else:       
        return sendMessage(client,message,"__Errore nella richiesta.\nEsaurite richieste giornaliere forse.__")
    return sendPhoto(client,message,image_url,"Ecco foto di volatile")
   
