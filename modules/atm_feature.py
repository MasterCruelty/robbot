import requests
import json
import sys
sys.path.append(sys.path[0] + "/..")
from utils.get_config import *
from pyrogram import Client

config = get_config_file("config.json")
api_url = config["api_url"]
api_get = config["api_get"]


"""
Restituisce l'elenco di tutte le fermate della linea richiesta con i codici corrispondenti
"""
def search_line(client,message,line_number):
    line = line_number.split(" ")
    line_number = line[0]
    try:
        direction = line[1]
    except:
        return sendMessage(client,message,"__Parametro direzione mancante__")
    request = "tpl/journeyPatterns/" + str(line_number) + "|" + direction
    get = api_get + "" + request
    resp = requests.get(get)
    data_json = handle_except(resp)
    if str(data_json).startswith("404"):
        return sendMessage(client,message,data_json)
    fermate = data_json["Stops"]
    description = data_json["Line"]["LineDescription"]
    result = "Linea **" + description + "** :\n\n<i>digita /atm 'codice' per sapere i dettagli di una fermata in particolare.</i>\n\n"
    for item in fermate:
        result += "**" + item["Description"] + "**" + " | codice: " + "<code>" + item["Code"] + "</code>\n\n"
    return sendMessage(client,message,result)



"""
    Dato un codice fermata, vengono fornite le informazioni relative a quella fermata contattando direttamente il server atm
    Dedicato ai dati delle fermate di mezzi di superficie/metro. Riporta dati parziali su altri tipi di richieste.
"""
def get_stop_info(stop_code,client,message):
    resp = get_json_atm(stop_code)
    data_json = handle_except(resp)
    if str(data_json).startswith("404"):
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

    result = "**" + descrizione + "**" + "\n"
    for i in range(len(line_code)):
        wait_time[i] = check_none(wait_time[i])
        result += line_code[i] + " " + line_description[i] + ": " + "**" + wait_time[i] + "**" + "\n"
    result += "\n"
    for i in range(len(line_code)):
        time_table[i] = check_none(time_table[i])
        result += "Orari linea " + line_code[i] + ": " + time_table[i] + "\n"
    return sendMessage(client,message,result)

"""
Restituisce i dati della rivendita richiesta.
"""
def get_rivendita_info(stop_code,client,message):
    resp = get_json_atm(stop_code)
    data_json = handle_except(resp)
    if str(data_json).startswith("404"):
        return sendMessage(client,message,data_json)
    descrizione = data_json["Description"]
    address = data_json["Address"]
    comune = data_json["Municipality"]
    dettagli = data_json["Details"]
    chiusura = dettagli["Giorno chiusura"]["Info"]
    servizi = dettagli["Servizi"]["Info"]
    result = "**"+descrizione+" "+address+" ("+comune+")**"+"\n"+"Giorno di chiusura: "+"**"+chiusura+"**"+"\n"+"Servizi: "+"**"+servizi+"**"
    return sendMessage(client,message,result)

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
    data = {"url": "tpPortal/geodata/pois/stops/" + stop_code + "?lang=it".format()}
    resp = requests.post(api_url,data = data)
    return resp

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
        result = "404: page not found"
        return result
    return data_json

