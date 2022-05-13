from pyrogram import Client
import utils.controller as uct
import utils.get_config as ugc
import random

"""
Lancia un sondaggio in automatico non anonimo
"""
@Client.on_message()
def poll_function(query,client,message):
    chat = ugc.get_chat(message)
    id_messaggio = ugc.get_id_msg(message)
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
def get_message(query,client,message):
    chat = ugc.get_chat(message)
    uct.save_json(message)
    client.send_document(chat,document = "json_message.json",caption = "__Ecco il json prodotto dal messaggio__",reply_to_message_id=message["message_id"])

"""
Veloce controllo se l'app è online
"""
def ping(query,client,message):
    return ugc.sendMessage(client,message,"pong" + query)

"""
documentazione dei comandi utente direttamente su Telegram
TO DO: rifattorizzare usando un dizionario
"""
def help(query,client,message):
    help_file = ugc.get_config_file("help.json")
    if "wiki" in query:
        help_wiki = help_file["wiki"][0]
        help_wikiall = help_file["wiki"][1]
        help_wikirandom = help_file["wiki"][2]
        help_comune = help_file["wiki"][3]
        return ugc.sendMessage(client,message,help_wiki+"\n\n"+help_wikiall+"\n\n"+help_wikirandom+"\n\n"+help_comune)
    if "lyrics" in query:
        help_lyrics = help_file["lyrics"]
        return ugc.sendMessage(client,message,help_lyrics)
    if "covid" in query:
        help_covid = help_file["covid"]
        return ugc.sendMessage(client,message,help_covid)
    if "vaccine" in query:
        help_vaccine = help_file["vaccine"]
        return ugc.sendMessage(client,message,help_vaccine)
    if "poll" in query:
        help_poll = help_file["poll"]
        return ugc.sendMessage(client,message,help_poll)
    if "atm" in query:
        help_atm = help_file["atm"][0]
        help_geoatm = help_file["atm"][1]
        help_searchatm = help_file["atm"][2]
        return ugc.sendMessage(client,message,help_atm+"\n\n"+help_geoatm+"\n\n"+help_searchatm)
    if "mappe" in query:
        help_map = help_file["mappe"][0]
        help_km = help_file["mappe"][1]
        return ugc.sendMessage(client,message,help_map+"\n\n" + help_km+"\n\n")
    if "meteo" in query:
        help_weather = help_file["meteo"][0]
        help_forecastoday = help_file["meteo"][1]
        help_forecastfuture = help_file["meteo"][2]
        help_weathermap = help_file["meteo"][3]
        return ugc.sendMessage(client,message,help_weather+"\n\n" + help_forecastoday+"\n\n"+help_forecastfuture+"\n\n"+help_weathermap)
    if "reminder" in query:
        help_reminder = help_file["reminder"]
        return ugc.sendMessage(client,message,help_reminder)
    if "openai" in query:
        help_openai = help_file["openai"]
        return ugc.sendMessage(client,message,help_openai)
    else:
        help_default = help_file["default"]
        return ugc.sendMessage(client,message,help_default)

"""
Restituisce 6 numeri tutti diversi tra loro tutti nel range da 1 a 90
"""
@Client.on_message()
def play_lotto(query,client,message):
    numbers = []
    while len(numbers) < 6:
        n = random.randint(1,90)
        if n not in numbers:
            numbers.append(n)
    result = '<code> '
    result += ' '.join(str(n) for n in numbers)
    result += ' </code>'
    return ugc.sendMessage(client,message,result)
