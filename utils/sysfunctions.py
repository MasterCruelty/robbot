from pyrogram import Client
import utils.utility
import utils.get_config
import utils.dbfunctions
import random
import time

"""
Lancia un sondaggio in automatico non anonimo
"""
@Client.on_message()
def poll_function(client,message,query):
    chat = utils.get_config.get_chat(message)
    id_messaggio = utils.get_config.get_id_msg(message)
    poll = query.split("/")
    domanda = poll[0]
    opzioni = poll[1]
    opzioni = opzioni.split(",")
    client.send_poll(chat,domanda,opzioni,is_anonymous=False,reply_to_message_id=id_messaggio)
    return

"""
Restituisce il json intero di un messaggio. Se il json supera la capacità di un messaggio Telegram, viene inviato sotto forma di file.
"""
@Client.on_message()
def get_message(client,message):
    chat = utils.get_config.get_chat(message)
    utils.utility.save_json(message)
    client.send_document(chat,document = "json_message.json",caption = "__Ecco il json prodotto dal messaggio__",reply_to_message_id=message["message_id"])

"""
Veloce controllo se l'app è online
"""
def ping(client,message):
    return utils.get_config.sendMessage(client,message,"pong")

"""
documentazione dei comandi utente direttamente su Telegram
"""
def help(client,message,query):
    help_file = utils.get_config.get_config_file("help.json")
    if "wiki" in query:
        help_wiki = help_file["wiki"][0]
        help_wikiall = help_file["wiki"][1]
        help_wikirandom = help_file["wiki"][2]
        help_comune = help_file["wiki"][3]
        return utils.get_config.sendMessage(client,message,help_wiki+"\n\n"+help_wikiall+"\n\n"+help_wikirandom+"\n\n"+help_comune)
    if "lyrics" in query:
        help_lyrics = help_file["lyrics"]
        return utils.get_config.sendMessage(client,message,help_lyrics)
    if "covid" in query:
        help_covid = help_file["covid"]
        return utils.get_config.sendMessage(client,message,help_covid)
    if "vaccine" in query:
        help_vaccine = help_file["vaccine"]
        return utils.get_config.sendMessage(client,message,help_vaccine)
    if "poll" in query:
        help_poll = help_file["poll"]
        return utils.get_config.sendMessage(client,message,help_poll)
    if "atm" in query:
        help_atm = help_file["atm"][0]
        help_edatm = help_file["atm"][1]
        help_geoatm = help_file["atm"][2]
        help_searchatm = help_file["atm"][3]
        return utils.get_config.sendMessage(client,message,help_atm+"\n\n"+help_edatm+"\n\n"+help_geoatm+"\n\n"+help_searchatm)
    if "mappe" in query:
        help_map = help_file["mappe"][0]
        help_km = help_file["mappe"][1]
        return utils.get_config.sendMessage(client,message,help_map+"\n\n" + help_km+"\n\n")
    if "meteo" in query:
        help_weather = help_file["meteo"][0]
        help_forecastoday = help_file["meteo"][1]
        help_forecastfuture = help_file["meteo"][2]
        return utils.get_config.sendMessage(client,message,help_weather+"\n\n" + help_forecastoday+"\n\n"+help_forecastfuture)
    if "reminder" in query:
        help_reminder = help_file["reminder"]
        return utils.get_config.sendMessage(client,message,help_reminder)
    else:
        return utils.get_config.sendMessage(client,message,"Cerca un comando in particolare come ad esempio:\n /helprob 'comando'\n__Comandi: wiki, lyrics, covid, vaccine,  meteo, poll, reminder atm e mappe.__")

"""
Restituisce 6 numeri tutti diversi tra loro tutti nel range da 1 a 90
"""
@Client.on_message()
def play_lotto(client,message):
    numbers = []
    while len(numbers) < 6:
        n = random.randint(1,90)
        if n not in numbers:
            numbers.append(n)
    result = ' '.join(str(n) for n in numbers)
    return utils.get_config.sendMessage(client,message,result)
