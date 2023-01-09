from utils.get_config import sendMessage,get_chat,get_id_msg 
from pyrogram import Client,filters,errors
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from pyrogram.handlers import CallbackQueryHandler
import re
import requests


"""
    restituisce la rivendita più vicina alla fermata cercata
"""
def get_tper_edicola(query,client,message):
    url = "https://hellobuswsweb.tper.it/web-services/hello-bus.asmx/QueryResale?fermata=" + str(query) + "&linea=&oraHHMM="
    data = requests.get(url)
    regex = re.findall('.asmx">([^<]*)',data.text)
    if("non trovata" in regex[0]):
        return sendMessage(client,message,"__404: page not found.__")
    data = regex[0].replace("fermata","fermata con codice ").split(":")
    result = "**" + data[0] + "**\n" + "__" + data[1] + "__"
    return sendMessage(client,message,result)

"""
    Restituisce i dati della fermata tper richiesta
"""
def get_tper_stop(query):
    fermata = query.split(" ")
    if(len(fermata) >1):
        url = "https://hellobuswsweb.tper.it/web-services/hello-bus.asmx/QueryHellobus?fermata=" + str(fermata[0]) + "&linea=" + str(fermata[1]) + "&oraHHMM="
    else: 
        url = "https://hellobuswsweb.tper.it/web-services/hello-bus.asmx/QueryHellobus?fermata=" + str(fermata[0]) + "&linea=&oraHHMM="
    data = requests.get(url)
    regex = re.findall('.asmx">([^<]*)',data.text)
    if("NON GESTITA" in regex[0]):
        return "__404: page not found.__"
    data = regex[0].replace("TperHellobus:","").replace("DaSatellite","da satellite") 
    info_stop = data.split(",")
    result = "**Fermata " + str(fermata[0]) + "**\n"
    for line in info_stop:
        result += "__Linea " + line + "__" + "\n"
    return result

"""
    Invia il messaggio con i dati della fermata tper costruendo il bottone inline per fare refresh
"""
@Client.on_message()
def send_tper_stop(query,client,message):
    result = get_tper_stop(query)
    if(result.startswith("__404")):
        return sendMessage(client,message,result)
    #build keyboard
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("Refresh",callback_data="REFRESH;"+str(query))]])
    #add handler
    client.add_handler(CallbackQueryHandler(callback=press_button,filters=filters.regex("REFRESH;"+str(query))))
    #send message with button
    client.send_message(get_chat(message),result,reply_markup=kb,reply_to_message_id=get_id_msg(message))

"""
    Rifà la richiesta sulla stessa fermata per aggiornare lo stato
"""
@Client.on_callback_query()
def press_button(client,message):
    cb = message.data.split(";")
    query = cb[1]
    print("Premuto bottone /tper con richiesta: " + str(query))
    #build keyboard
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("Refresh",callback_data="REFRESH;"+str(query))]])
    #refresh
    try:
        message.edit_message_text(get_tper_stop(query),reply_markup=kb)
    except errors.exceptions.bad_request_400.MessageNotModified:
        message.edit_message_text(get_tper_stop(query)+"\n__Nessun aggiornamento per ora__",reply_markup=kb)

