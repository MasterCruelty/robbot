from utils.get_config import sendMessage,get_chat,get_id_msg,sendPhoto
from pyrogram import Client,errors
import requests
from bs4 import BeautifulSoup
import re



"""
    Restituisce una stima sullo stipendio netto annuale e mensile data la ral annua e la regione in cui viene percepita.
    L'addizionale del comune applicata è quella del comune di Milano(0.8%)
    Il tutto è calcolato su 13 mensilità e supponendo un datore di lavoro privato
"""
def ral_calc(query,client,message):
    splitted = query.split(" ")
    ral = splitted[0]
    if not ral.isdigit():
        return sendMessage(client,message,"Errore formato.\nScopri di più con __/helprob ral__")
    if len(splitted) > 1:
        region = splitted[1].lower()
    else:
        region = "lombardia"
    url = "https://www.pmi.it/servizi/292472/calcolo-stipendio-netto.html?step=2&ral=" + ral + "&reg=" + region + "&com=0.8&car=no&child_noau=0&child_au=0&childh=0&childcharge=100&family=0&monthlypay=13&days=365"
    resp = requests.get(url)
    zuppa = BeautifulSoup(resp.text,"html.parser")
    tags = zuppa.find_all("div",attrs={"class": "income-results tbm-pdf-download"})
    results = [tag.getText() for tag in tags if tag.getText() != ""]
    pattern = r"Stipendio netto annuo([\d.]+) €Stipendio netto mensile([\d.]+) €"
    match = re.search(pattern,results[0])
    result = "Ecco la stima che desideravi:\n\n"
    if match:
        complessivo = match.group(1)
        mensile = match.group(2)
        output = f"Stipendio complessivo {complessivo} € \n" \
                 f"Stipendio mensile {mensile} € \n"
        result += "__" + output + "__"
        return sendMessage(client,message,result)
    else:
        return sendMessage(client,message,"__404: not found__")
        
