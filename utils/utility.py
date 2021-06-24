import time
import os
from pyrogram import Client
import utils_config
import modules.wiki
import modules.lyrics
import modules.atm_feature
import modules.covid
import modules.gmaps
import modules.weather
import modules.reminder
import utils.dbfunctions
import utils.sysfunctions
import utils.get_config

"""
Questa funzione prende come argomento il match e la richiesta dal main e dirotta la richiesta sul file dedicato a quel comando
"""
def fetch_command(match,query,client,message):
    if match == "/wiki" :
        return modules.wiki.execute_wiki(query,client,message)
    if match == "/lyrics":
        return modules.lyrics.execute_lyrics(query,client,message)
    if match == "/atm":
        return modules.atm_feature.get_stop_info(query,client,message)
    if match == "/geoatm":
        return modules.atm_feature.geodata_stop(query,client,message)
    if match == "/edatm":
        return modules.atm_feature.get_rivendita_info(query,client,message)
    if match == "/searchatm":
        return modules.atm_feature.search_line(client,message,query)
    if match == "/covid":
        return modules.covid.covid_cases(client,message,query)
    if match == "/vaccine":
        return modules.covid.check_vaccine_function(client,message,query)
    if match == "/poll":
        return utils.sysfunctions.poll_function(client,message,query)
    if match == "/helprob":
        return utils.sysfunctions.help(client,message,query)
    if match == "/map":
        return modules.gmaps.showmaps(query,client,message)
    if match == "/km":
        return modules.gmaps.execute_km(query,client,message)
    if match == "/weather":
        return modules.weather.get_weather(client,message,query)
    if match == "/forecastoday":
        return modules.weather.get_today_forecasts(client,message,query)
    if match == "/forecastfuture":
        return modules.weather.get_future_forecasts(client,message,query)
    if match == "/reminder":
        return modules.reminder.set_reminder(client,message,query)

"""
Analogamente a fetch_command ma per i comandi esclusivi degli utenti admin
"""
def fetch_admin_command(match,query,client,message):
    #system functions
    if match == "/getmessage":
        return utils.sysfunctions.get_message(client,message)
    if match == "/playlotto":
        return utils.sysfunctions.play_lotto(client,message)
    if match == "/pingrob":
        return utils.sysfunctions.ping(client,message)

"""
Analogamente a fetch_command ma per i comandi esclusivi del super admin
"""
def fetch_super_command(match,query,client,message):
    #db functions
    if match == "/setrobuser":
        return utils.dbfunctions.set_user(client,message,query)
    if match == "/delrobuser":
        return utils.dbfunctions.del_user(client,message,query)
    if match == "/listrobuser":
        return utils.dbfunctions.list_user(client,message)
    if match == "/allrobuser":
        return utils.dbfunctions.all_user(client,message)
    if match == "/setrobadmin":
        return utils.dbfunctions.set_admin(client,message,query)
    if match == "/delrobadmin":
        return utils.dbfunctions.del_admin(client,message,query)
    
"""
funzione che aiuta a parsare i comandi nel sorgente principale senza sporcare troppo in giro
"""
def parser(message):
    temp = message.split(" ",1)
    try:
        result = temp[1]
    except:
        result = temp[0]
    return result

"""
	funzione che salva su file il json del messaggio Telegram in arrivo
"""
def save_json(message):
    nome_file = "json_message.json"
    save = open(nome_file,'w')
    save.write(str(message))
    save.close()
"""
	funzione per visualizzare a schermo i dati principali del messaggio in arrivo
"""
def visualizza(chat,nome_chat,utente,nome_utente,username,messaggio):
    print("id_utente: " + str(utente) + "\nnome_utente: " + nome_utente + "\nusername: " + username)
    try:
        print("chat_id: " + str(chat) + "\nnome_chat: " + nome_chat)
    except:
        print("messaggio ricevuto da un channel o chat privata")
    print("\n\nMessaggio: " + messaggio + "\n" )
    print("**************************************************************************************")
    if str(chat):
        return "nome_chat: " + str(chat) +"id_utente: " + str(utente) + "\nnome_utente: " + nome_utente + "\nusername: " + username + "\n\n" + "Messaggio: " + messaggio
