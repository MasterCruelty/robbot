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
    url = "http://www.viaggiatreno.it/infomobilita/resteasy/viaggiatreno/autocompletaStazione/" + name
    resp = requests.get(url)
    data = resp.text.split("|")
    station_code = data[1].replace("\n","")
    try:
        int(station_code[1:])
    except ValueError:
        return sendMessage(client,message,"__Stazione " + name +" non trovata__")
    return station_code

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
    from_station = get_station_code(client,message,splitted[0])
    to_station = get_station_code(client,message,str(splitted[1])[1:]) #da pos 1 perché c'è uno spazio
    if len(splitted) < 3:
        now = str(datetime.datetime.now())
        date_time = now.replace(" ","T")
    else:
        date_time = splitted[2] + "T00:00:00"
    #formatto i codici stazione per essere in regola per la chiamata dopo
    from_station = from_station.replace("S","")
    to_station = to_station.replace("S","")
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
    data = json.loads(resp.text)
    data = data["soluzioni"]
    pages = []
    result = "**__" + date_time + "__**\n\n"
    i = 0
    for item in data:
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
        if i == 3:
            pages.append(result)
            result = "**__" + date_time + "__**\n\n"
            i = 0

    #build keyboard
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("Prossimi treni",callback_data="PROSSIMI")]])
    
    #add handler
    client.add_handler(CallbackQueryHandler(callback=press_button,filters=filters.regex("PROSSIMI")))
    k = 0
    client.send_message(get_chat(message),pages[k],reply_markup=kb,reply_to_message_id=get_id_msg(message))

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


