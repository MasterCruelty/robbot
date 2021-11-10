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

dictionary = {      '/wiki'           : modules.wiki.execute_wiki,
                    '/map'            : modules.gmaps.showmaps,
                    '/km'             : modules.gmaps.execute_km,
                    '/lyrics'         : modules.lyrics.execute_lyrics,
                    '/atm'            : modules.atm_feature.get_stop_info,
                    '/geoatm'         : modules.atm_feature.geodata_stop,
                    '/searchatm'      : modules.atm_feature.search_line,
                    '/covid'          : modules.covid.covid_cases,
                    '/vaccine'        : modules.covid.check_vaccine_function,
                    '/poll'           : utils.sysfunctions.poll_function,
                    '/weather'        : modules.weather.get_weather,
                    '/forecastoday'   : modules.weather.get_today_forecasts,
                    '/forecastfuture' : modules.weather.get_future_forecasts,
                    '/reminder'       : modules.reminder.set_reminder,
                    '/mystat'         : utils.dbfunctions.show_stats,
                    '/helprob'        : utils.sysfunctions.help}

dictionary_admin = {'/getmessage'     : utils.sysfunctions.get_message,
                    '/playlotto'      : utils.sysfunctions.play_lotto,
                    '/pingrob'        : utils.sysfunctions.ping}

dictionary_super = {'/setrobuser'     : utils.dbfunctions.set_user,
                    '/delrobuser'     : utils.dbfunctions.del_user,
                    '/listrobuser'    : utils.dbfunctions.list_user,
                    '/allrobuser'     : utils.dbfunctions.all_user,
                    '/setrobadmin'    : utils.dbfunctions.set_admin,
                    '/delrobadmin'    : utils.dbfunctions.del_admin}

"""
Questa funzione prende come argomento il match e la richiesta dal main e dirotta la richiesta sul file dedicato a quel comando
"""
def fetch_command(match,query,client,message):
    utils.dbfunctions.update_stats(utils.get_config.get_id_user(message),match)
    if match in dictionary:
        dictionary[match](query,client,message)
"""
Analogamente a fetch_command ma per i comandi esclusivi degli utenti admin
"""
def fetch_admin_command(match,query,client,message):
    #system functions
    if match in dictionary_admin:
        dictionary_admin[match](client,message)

"""
Analogamente a fetch_command ma per i comandi esclusivi del super admin
"""
def fetch_super_command(match,query,client,message):
    #db functions
    if match in dictionary_super:
        try:
            dictionary_super[match](client,message,query)
        except:
            dictionary_super[match](client,message)
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
