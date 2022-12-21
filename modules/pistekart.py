from utils.get_config import sendMessage,get_chat,get_id_msg 
from pyrogram import Client,filters,errors
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from pyrogram.handlers import CallbackQueryHandler
import re
import requests
from bs4 import BeautifulSoup



"""
    Restituisce i dati di tutte le piste in una regione o provincia se specificata
    Nel formato /piste <region> <provincia> oppure /piste <region>
"""
def get_piste_region(query,client,message):
    if " " in query:
        splitted = query.split(" ")
        url ="https://pistekartitalia.it/piste/" + splitted[0] + "/" + splitted[1]
    else:
        url = "https://pistekartitalia.it/piste/" + query
    resp = requests.get(url)
    zuppa = BeautifulSoup(resp.text,"html.parser")
    tags = zuppa.find_all(("div","h2"),attrs={"class":"field-content"})
    results = [tag.getText() for tag in tags if tag.getText() != ""]

    pista = ""
    piste = []
    result = ""
    for i in range(len(results)):
        if "\n\n" in results[i] :
            continue
        if len(results[i].replace(" ","")) == 5 and results[i].replace(" ","").isdigit():
            pista += results[i] + "\n"
            piste.append(pista)
            result += pista + "\n\n"
            pista = ""
        else:
            pista += results[i] + "\n"

    try:
        return sendMessage(client,message,result)
    except errors.exceptions.bad_request_400.MessageEmpty:
        return sendMessage(client,message,"__Pagina non trovata__")


