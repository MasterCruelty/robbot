from pyrogram import Client
from pyrogram import errors
import utils.controller as uct
import utils.get_config as ugc
import random
import os
import sys

"""
Lancia un sondaggio in automatico non anonimo
"""
@Client.on_message()
def poll_function(query,client,message):
    chat = ugc.get_chat(message)
    id_messaggio = ugc.get_id_msg(message)
    poll = query.split("/")
    domanda = poll[0]
    try:
        opzioni = poll[1]
        opzioni = opzioni.split(",")
        client.send_poll(chat,domanda,opzioni,is_anonymous=False,reply_to_message_id=id_messaggio)
    except (IndexError,errors.exceptions.bad_request_400.PollAnswersInvalid,Exception):
        return ugc.sendMessage(client,message,"__Errore formato.\n/helprob poll__")

"""
Restituisce il json intero di un messaggio. Se il json supera la capacità di un messaggio Telegram, viene inviato sotto forma di file.
"""
@Client.on_message()
def get_message(query,client,message):
    chat = ugc.get_chat(message)
    uct.save_json(message)
    client.send_document(chat,document = "json_message.json",caption = "__Ecco il json prodotto dal messaggio__",reply_to_message_id=message.id)

"""
Veloce controllo se l'app è online
"""
def ping(query,client,message):
    return ugc.sendMessage(client,message,"pong " + query.replace("/pingrob",""))

"""
Riavvia il bot
"""
def restart(client,message):
    ugc.sendMessage(client,message,"__Riavviando...\n\nTra circa 10 secondi dovrei essere di nuovo attivo.__")
    os.execl(sys.executable,sys.executable,*sys.argv)

"""
documentazione dei comandi utente direttamente su Telegram
"""
def help(query,client,message):
    help_file = ugc.get_config_file("help.json")
    if query in help_file:
        help_request = help_file[query][0:]
        help_request = str(help_request).replace("(","").replace(")","").replace('"','').replace(r'\n','\n')
        return ugc.sendMessage(client,message,help_request)
    elif (query not in help_file) and (query != "/helprob"):
        help_request = "__**Comando non trovato**__\n\n"
        help_request += help_file["default"]
        return ugc.sendMessage(client,message,help_request)
    else:
        help_request = help_file["default"]
        return ugc.sendMessage(client,message,help_request)

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
