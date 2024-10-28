import requests
import json
import sys
import time
sys.path.append(sys.path[0] + "/..")
from utils.get_config import *
from pyrogram import Client,filters,errors
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from pyrogram.handlers import CallbackQueryHandler
import pdf2image
import io
import re

config = get_config_file("config.json")
api_url = config["api_url"]
api_get = config["api_get"]
cookie = config["cookie"]
cookie_parts = cookie.split("=")
cookie = {cookie_parts[0]: cookie_parts[1]}
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "it-IT,it;q=0.9,de-DE;q=0.8,de;q=0.7,en-US;q=0.6,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Upgrade-Insecure-Requests": "1",
    "Sec-CH-UA": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1"
}
cookies = {'cookie_name': cookie}

#strighe costanti da usare in certe situazioni
not_available = "Non disponibile"
pdfimage = "pdf2image"

"""
Restituisce l'elenco delle fermate dato l'indirizzo richiesto con i codici fermata corrispondenti
"""
def search_line(line_number,client,message):
    stops = search_stop(line_number)
    #Faccio un controllo sul fatto che l'array abbia effettivamente trovato un json, altrimenti messaggio senza risultati
    if "fermata trovata" in stops:
        return sendMessage(client,message,stops)
    result = str(len(stops)) + " risultati:\n<i>digita /atm 'codice' per sapere i dettagli di una fermata in particolare.</i>\n\n"
    for item in stops:
        if item["Lines"] == []:
            result += "**" + item["Description"] + "(" + item["Municipality"] + ")**" + " | codice: " + "<code>" + item["CustomerCode"] + "</code>\n\n"
            continue
        result += "__**Linea " + item["Lines"][0]["Line"]["LineCode"]  + " " + item["Lines"][0]["Line"]["LineDescription"]+"__**\n"
        result += "**" + item["Description"] + "(" + item["Municipality"] + ")**" + " | codice: " + "<code>" + item["CustomerCode"] + "</code>\n\n"
    return sendMessage(client,message,result)


"""
    Restituisce la tabella degli orari come immagine dato l'url pdf
"""
def get_time_table(client,message,pdf_url):
    pdf_data = requests.get(pdf_url)
    img_data = pdf2image.convert_from_bytes(pdf_data.content,fmt="png")
    if img_data:
        for i, img in enumerate(img_data):
            with io.BytesIO() as img_buffer:
                img.save(img_buffer, format="PNG")
                img_buffer.name = f"time_table_page_{i + 1}.png"
                sendPhoto(client, message, img_buffer, "__Tabella degli orari per la linea {}__".format(estrai_numero_linea(pdf_url)))
    else:
        sendMessage(client,message,"__Nessun pdf degli orari trovato per questa fermata.__")

"""
    funzione ausiliaria per estrarre il numero della linea dal link della time table.
    Utilizzata in get_time_table
"""
def estrai_numero_linea(link):
    # Utilizza un'espressione regolare per cercare il numero della linea nel link
    match = re.search(r'(\d+)_\d+\.pdf', link)

    if match:
        # Restituisci il primo gruppo corrispondente (il numero della linea)
        return match.group(1)
    else:
        # Restituisci None se non viene trovato nessun match
        return None
"""
    Dato un codice fermata, vengono fornite le informazioni relative a quella fermata contattando direttamente il server atm
    Dedicato ai dati delle fermate di mezzi di superficie/metro. Riporta dati parziali su altri tipi di richieste.
"""
def get_stop_info(stop_code,client=None,message=None):
    #bool per fissare se l'utente vuole il tempo d'attesa oppure la tabella degli orari come immagine
    checkT = False
    if "-t" in stop_code:
        stop_code = stop_code.split("-t")[1].replace(" ","")
        checkT = True
    resp = get_json_atm(stop_code)
    data_json = handle_except(resp)
    
    #############################
    #In caso di malfunzionamento del comando, provare a de-commentare la riga seguente
    #sendMessage(client,message,data_json)
    #############################
    
    if str(data_json).startswith("404") or "riprova tra poco" in str(data_json):
        return sendMessage(client,message,data_json)
    descrizione = data_json["Description"]
    Lines = data_json["Lines"]
    line_code, line_description, wait_time, time_table = ([] for i in range(4))
    for item in Lines:
        Line = item["Line"]
        line_code.append(Line["LineCode"])
        line_description.append(Line["LineDescription"])
        wait_time.append(item["WaitMessage"])
        time_table.append(item["BookletUrl"])
    #controllo se l'utente vuole solo la tabella degli orari
    if checkT == True:
        for i in range(len(time_table)):
            get_time_table(client,message,time_table[i])
        return pdfimage
    result = "**" + descrizione + "**" + "\n"
    for i in range(len(line_code)):
        wait_time[i] = check_none(wait_time[i])
        result += line_code[i] + " " + line_description[i] + ": " + "**" + wait_time[i] + "**" + "\n"
    result += "\n"
    for i in range(len(line_code)):
        time_table[i] = check_none(time_table[i])
        #Se non c'è il tempo d'attesa, mando gli orari del pdf come immagine
        if wait_time[i] == not_available and time_table[i] != not_available:
            #scarico gli orari con una get, poi converto in immagine in memory senza scrivere su disco con get_time_table definita qui sopra
            pdf_url = time_table[i]
            sendMessage(client,message,"__WaitTime non disponibile, inviando la tabella degli orari tra una manciata di secondi...__")
            checkT = True
            get_time_table(client,message,pdf_url)
            #stringa da restituire così che la funzione send_stop_info sappia che è già stata mandata la tabella degli orari come immagine
        result += "Orari linea " + line_code[i] + ": " + time_table[i] + "\n"
    if checkT == True:
        return pdfimage
    return result

"""
    Invia il messaggio con i dati della fermata atm con bottone inline refresh
"""
@Client.on_message()
def send_stop_info(query,client,message):
    #get data
    result = get_stop_info(query,client,message)
    #se la condizione è vera, allora è stata inviata la tabella degli orari come immagine da get_stop_info()
    if str(result) == pdfimage:
        return
    #build keyboard
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("Refresh",callback_data="REFRESH;"+str(query))]])
    #add handler
    client.add_handler(CallbackQueryHandler(callback=press_button,filters=filters.regex("REFRESH;"+str(query))))
    #send message with button
    client.send_message(get_chat(message),result,reply_markup=kb,disable_web_page_preview=True,reply_to_message_id=get_id_msg(message))

"""
    Aggiorna lo stato sulla fermata
"""
@Client.on_callback_query()
def press_button(client,message):
    cb = message.data.split(";")
    query = cb[1]
    print("bottone atm premuto con richiesta: " + str(query))
    #build keyboard
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("Refresh",callback_data="REFRESH;"+str(query))]])
    #edit message
    try:
        message.edit_message_text(get_stop_info(query,client,message),reply_markup=kb,disable_web_page_preview=True)
    except errors.exceptions.bad_request_400.MessageNotModified:
        message.edit_message_text(get_stop_info(query,client,message)+"\n__Nessun aggiornamento per ora__",reply_markup=kb,disable_web_page_preview=True)
        time.sleep(5)
        


"""
dato un codice fermata, fornisce le coordinate geografiche di quella fermata.
Funziona con qualsiasi tipo di oggetto, dalla fermata del bus al parchimetro.
"""
@Client.on_message()
def geodata_stop(stop_code,client,message):
    resp = get_json_atm(stop_code)
    data_json = handle_except(resp)
    if str(data_json).startswith("404"):
        return sendMessage(client,message,data_json)
    coords = data_json["Location"]
    latitud = coords["Y"]
    longitud= coords["X"]
    client.send_location(get_chat(message),latitud,longitud,reply_to_message_id=get_id_msg(message))
    return

"""
Fa la richiesta al server atm e restituisce il json corrispondente.
"""
def get_json_atm(stop_code):
    url = api_url + 'tpPortal/geodata/pois/stops/' + stop_code
    #data = {"url": "tpPortal/geodata/pois/stops/" + stop_code + "?lang=it".format()}
    try:
        #resp = requests.post(api_url,data = data,headers = headers,cookies = cookies)
        resp = requests.get(url,headers=headers,cookies=cookie)
    except requests.exceptions.ConnectionError as e:
        return "__Troppe richieste, riprova tra poco.__"
    return resp

"""
cerca qualsiasi fermata esistente a partire da un indirizzo
"""
def search_stop(query):
    url = api_url + 'tpPortal/tpl/stops/search/' + query
    #data = {"url": "tpPortal/tpl/stops/search/" + query + "".format()}
    stops = []
    try:
        #for stop in (requests.post(api_url,data = data,headers = headers,cookies=cookies)).json():
        for stop in (requests.get(url,headers=headers,cookies=cookie)).json():
            stops.append(stop)
    except:
        result = "__Nessuna fermata trovata.__"
        return result
    return stops

"""
Controlla se un campo estratto del json è nullo per evitare eccezioni sul concatenamento di stringhe.
"""
def check_none(field):
    if field is None:
        return "Non disponibile"
    else:
        return field
"""
cattura eventuali eccezioni sulle richieste.
"""
def handle_except(resp):
    try:
        data_json = resp.json()
    except:
        result = "Funzione non più supportata fino a data da destinarsi"
        return result
    return data_json

