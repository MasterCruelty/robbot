import time
from datetime import date
from pyrogram import Client 
from utils.utility import *
from utils.dbfunctions import *
from utils.get_config import get_config_file,get_username,get_text_message,get_chat,get_id_msg,get_id_user,get_first_name
from utils.sysfunctions import *

config = get_config_file("config.json")
api_id = config["api_id"]
api_hash = config["api_hash"]
bot_token = config["bot_token"]
session = config["session_name"]
comandi = config["commands"][0]
comandi_admin = config["commands"][1]
comandi_super = config["commands"][2]
app = Client(session, api_id, api_hash,bot_token)

@app.on_message()
def print_updates(client,message):
    #recupero parametri principali del messaggio dal json
    chat = get_chat(message)
    id_messaggio = get_id_msg(message)
    utente = get_id_user(message)
    nome_chat = message["chat"]["title"]
    nome_utente = get_first_name(message)
    time_message = time.strftime("%H:%M:%S")
    username = get_username(message) 
    messaggio = get_text_message(message)

    
    #Restituisce il json del messaggio
    if "/getmessage" in str(message) and (isAdmin(utente) or isSuper(utente)):
        return get_message(client,message)

    #funzionalità super admin
    cmd_super = comandi_super.split(";")
    match = messaggio.split(" ")
    if match[0] in cmd_super and isSuper(utente):
    #rappresentazione grafica del messaggio corrente sul terminale
        visualizza(chat,nome_chat,utente,nome_utente,username,messaggio)
        query = parser(messaggio)
        fetch_super_command(match[0],query,client,message)
        return

    #funzionalità admin
    cmd_admin = comandi_admin.split(";")
    match = messaggio.split(" ")
    if match[0] in cmd_admin and isAdmin(utente):
    #rappresentazione grafica del messaggio corrente sul terminale
        visualizza(chat,nome_chat,utente,nome_utente,username,messaggio)
        query = parser(messaggio)
        fetch_admin_command(match[0],query,client,message)
        return

    #funzionalità per gli utenti
    lista_comandi = comandi.split(";")
    match = messaggio.split(" ")
    if match[0] in lista_comandi and isUser(utente):
    #rappresentazione grafica del messaggio corrente sul terminale
        visualizza(chat,nome_chat,utente,nome_utente,username,messaggio)
        query = parser(messaggio)
        fetch_command(match[0],query,client,message)
        return
    elif match[0] in lista_comandi or messaggio == "/start":
        app.send_message(chat,"Se vuoi usare uno dei miei comandi, devi essere registrato.\nContatta @MasterCruelty")

app.run()
