from utils.get_config import sendMessage
from pyrogram import Client,errors
import requests
import json

"""
    Restituisce una barzelletta casuale.
    Aggiungendo l'opzione -c è possibile filtrare per una categoria.
"""
def get_random_joke(query,client,message):
    if "-c" in query:
        category = query.split(" ")[1]
        if category.title() == "Misc":
            category = "Miscellaneous"
        url = "https://v2.jokeapi.dev/joke/" + category.title()
    else:
        url = "https://v2.jokeapi.dev/joke/Any"
    resp = requests.get(url)
    data = json.loads(resp.text)
    result ="__Errore nella richiesta del joke.__"
    if data["type"] == "single":
        result = "**" + data["joke"] + "**"
    else:
        first = "**" + data["setup"] + "**"
        second = "|| __" + data["delivery"] + "__ ||"
        result = first + second
    return sendMessage(client,message,result)
        



