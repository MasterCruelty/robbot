from utils.get_config import sendMessage,sendPhoto
from pyrogram import Client,errors
import requests
import json


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
