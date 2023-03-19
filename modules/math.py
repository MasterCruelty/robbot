from utils.get_config import sendMessage,get_chat,get_id_msg
from pyrogram import Client,errors
import requests


"""
    Restituisce il risultato dell'espressione matematica richiesta
"""
def calculate(query,client,message):
    url = "http://api.mathjs.org/v4/?expr=" + query
    if "/" in query:
        url += "&precision=3"
    resp = requests.get(url)
    return sendMessage(client,message,resp.text) 
