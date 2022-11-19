from utils.get_config import sendMessage,get_chat,get_id_msg 
from pyrogram import Client,filters,errors
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from pyrogram.handlers import CallbackQueryHandler
import requests
import json
import datetime



"""
    Restituisce il codice stazione della stazione richiesta
"""
def get_station_code(client,message,name):
    url = "http://www.viaggiatreno.it/infomobilita/resteasy/viaggiatreno/cercaStazione/" + name
    resp = requests.get(url)
    try:
        data = json.loads(resp.text)
    except json.decoder.JSONDecodeError:
        return None 
    #vedo se tra i risultati trovati c'è il nome della stazione cercato e restituisco il suo codice stazione
    for item in data:
        if name.upper() in item["nomeLungo"] or name.title() in item["nomeBreve"]:
            return item["id"]
    return None 

"""
    Restituisce la stazione di partenza del treno indicato
"""
def departStation_train(client,message,train_number):
    url = "http://www.viaggiatreno.it/infomobilita/resteasy/viaggiatreno/cercaNumeroTreno/" + train_number
    resp = requests.get(url)
    if resp.text == '':
        return sendMessage(client,message,"__Treno non trovato__")
    data = json.loads(resp.text)
    return "Stazione di partenza del treno "+ train_number + ": " + data["codLocOrig"] + " " + data["descLocOrig"]



"""
    Restituisce i dati delle partenze di treni che vanno da una stazione A a una stazione B con gli orari e altre info
"""
global pages
global k

@Client.on_message()
def timetable2stations(query,client,message):
    global pages
    global k
    splitted = query.split(",")
    try:
        from_station = get_station_code(client,message,splitted[0])
        to_station = get_station_code(client,message,str(splitted[1])[1:]) #da pos 1 perché c'è uno spazio
    except IndexError:
        return sendMessage(client,message,"__Errore formato.\nProva /helprob trenitalia__")
    if len(splitted) < 3:
        now = str(datetime.datetime.now())
        date_time = now.replace(" ","T")
    else:
        date_time = splitted[2] + "T00:00:00"
    #formatto i codici stazione per essere in regola per la chiamata dopo
    try:
        from_station = from_station.replace("S","")
        to_station = to_station.replace("S","")
    except AttributeError:
        return sendMessage(client,message,"__Stazione " + name +" non trovata__")
    #rimuovo il carattere S e i primi zeri che compaiono altrimenti non va a buon fine la richiesta
    while True:
        if from_station.startswith("0"):
            from_station = from_station[1:]
        elif to_station.startswith("0"):
            to_station = to_station[1:]
        else:
            break
    url = "http://www.viaggiatreno.it/infomobilita/resteasy/viaggiatreno/soluzioniViaggioNew/" + from_station + "/" + to_station + "/" + date_time
    resp = requests.get(url)
    if resp.text == 'Error':
        return sendMessage(client,message,"__Errore formato.\nProva /helprob treni__")
    data_complete = json.loads(resp.text) #questo json contiene anche origine e destinazione predefinite
    data = data_complete["soluzioni"] #questo json contiene solo le soluzioni di viaggio dirette e con cambi
    pages = []
    result = "**__" + date_time.split("T")[0] + "__**\n\n"
    i = 0
    #il json ottenuto è composto da n oggetti di tipo "vehicles" ognuno dei quali contenenti una lista di oggetti.
    #Se il treno è diretto è uno solo, ma se ha dei cambi sono più di uno, quindi controllo che la destinazione 
    #corrisponda con quella richiesta.
    check_cambi = False
    for item in data:
        if item["vehicles"][0]["destinazione"] == data_complete["destinazione"]:
            from_s = item["vehicles"][0]["origine"]
            from_time = str(item["vehicles"][0]["orarioPartenza"].split("T")[1])[0:5]
            to_time = str(item["vehicles"][0]["orarioArrivo"].split("T")[1])[0:5]
            to_s = item["vehicles"][0]["destinazione"]
            durata = item["durata"]
            tipo_treno = item["vehicles"][0]["categoriaDescrizione"]
            numero_treno = item["vehicles"][0]["numeroTreno"]
            result += "**" + from_s + "==>" + to_s + "(" + from_time + "-" + to_time + ")**\n"
            result += "__Treno: " + tipo_treno + " " + numero_treno + "__\n"
            result += "**Durata: " + str(durata) + "**\n\n"
            i += 1
            if i == 3 or check_cambi == True: #per visualizzare almeno 3 soluzioni consecutive dirette o solo una se ci sono spesso cambi necessari
                pages.append(result)
                if item["vehicles"][0]["orarioPartenza"].split("T")[0] == date_time:
                    result = "**__" + date_time.split("T")[0] + "__**\n\n"
                else:
                    result = "**__" + item["vehicles"][0]["orarioPartenza"].split("T")[0] + "__**\n\n"
                i = 0
                check_cambi = False
        else:
            check_cambi = True
            result = "__Questa soluzione presenta dei cambi__\n\n"
            durata = item["durata"]
            for cambio in item["vehicles"]:
                from_s = cambio["origine"]
                from_time = str(cambio["orarioPartenza"].split("T")[1])[0:5]
                to_time = str(cambio["orarioArrivo"].split("T")[1])[0:5]
                to_s = cambio["destinazione"]
                tipo_treno = cambio["categoriaDescrizione"]
                numero_treno = cambio["numeroTreno"]
                result += "**" + from_s + "==>" + to_s + "(" + from_time + "-" + to_time + ")**\n"
                result += "__Treno: " + tipo_treno + " " + numero_treno + "__\n\n"
            result += "**Durata: " + str(durata) + "**\n\n"
            pages.append(result)
            i = 0
            if item["vehicles"][0]["orarioPartenza"].split("T")[0] == date_time:
                result = "**__" + date_time.split("T")[0] + "__**\n\n"
            else:
                result = "**__" + item["vehicles"][0]["orarioPartenza"].split("T")[0] + "__**\n\n"
        

    #build keyboard
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("Prossimi treni",callback_data="PROSSIMI")]])
    
    #add handler
    client.add_handler(CallbackQueryHandler(callback=press_button,filters=filters.regex("PROSSIMI")))
    k = 0
    try:
        client.send_message(get_chat(message),pages[k],reply_markup=kb,reply_to_message_id=get_id_msg(message))
    except IndexError:
        return sendMessage(client,message,"__Errore formato.\nProva /helprob treni__")


"""
    funzione callback per il bottone "prossimi treni" che fa visualizzare la pagina successiva
"""
@Client.on_callback_query(filters = filters.regex("PROSSIMI"))
def press_button(client,message):
    global k
    if k < len(pages)-1:
        k = k + 1
        kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("Prossimi treni",callback_data="PROSSIMI")]])
        message.edit_message_text(pages[k],reply_markup=kb)
    else:
        message.edit_message_text("__Fine__")


def get_delay(query,client,message):
    url = "http://www.viaggiatreno.it/infomobilita/resteasy/viaggiatreno/partenze/"
    splitted = query.split(",")
    station_code = get_statio_code(splitted[1])
    train_number = splitted[0]
    url += station_code + "/" + train_number
    date_obj = datetime.now()
    week_day = date_obj.strftime('%a')
    month = date_obj.strftime('%b')
    month_day = date_obj.strftime('%d')
    year = date_obj.strftime('%Y')
    date_time = datetime.datetime.now().split(".")[0]
    date_time += " GMT+0100 (Ora standard dell'Europa centrale)"
