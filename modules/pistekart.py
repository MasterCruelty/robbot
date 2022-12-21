from utils.get_config import sendMessage,get_chat,get_id_msg,sendPhoto
from pyrogram import Client,errors
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

"""
    restituisce informazioni dettagliate sulla pista scelta, inclusa la foto del tracciato
"""
def get_info_pista(query,client,message):
    url = "https://www.pistekartitalia.it/" + query.replace(" ","-")
    resp = requests.get(url)
    
    #recupero della foto del tracciato
    zuppa = BeautifulSoup(resp.text,"html.parser")
    images = zuppa.select('div img')
    img_url = images[len(images)-1]['src']

    #recupero descrizione pista
    try:
        info_track = zuppa.find_all("div",attrs={"class":"circuit-information"})
        info_track = [tag.getText() for tag in info_track]
        info_track = info_track[0].rsplit('Mappa',1)
        info_track = info_track[0]
    except IndexError:
        info_track = "__Descrizione pista non disponibile__"
    
    #invio messaggio con descrizione pista e foto tracciato
    sendMessage(client,message,"__" + info_track+ "__")
    sendPhoto(client,message,img_url,"__Foto del tracciato__")

