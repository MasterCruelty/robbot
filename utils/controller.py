from pyrogram import Client
import utils_config
import modules.wiki
import modules.lyrics
import modules.atm_feature
import modules.covid
import modules.gmaps
import modules.weather
import modules.reminder
import modules.openai
import modules.urban
import modules.tper
import modules.viaggiatreno
import modules.trivial
import modules.pistekart
import modules.ingv
import modules.ral
import modules.math
import modules.animals
import modules.videodl
import modules.latex
import modules.passport
import modules.weatherextreme
import modules.space
import modules.bgg
import modules.flight
import modules.jokes
import utils.dbfunctions as udb
import utils.sysfunctions as usys
import utils.get_config as ugc

#Dizionario con l'elenco dei comandi utente
dictionary = {      '/wiki'           : modules.wiki.execute_wiki,
                    '/map'            : modules.gmaps.showmaps,
                    '/km'             : modules.gmaps.execute_km,
                    '/lyrics'         : modules.lyrics.execute_lyrics,
                    '/atm'            : modules.atm_feature.send_stop_info,
                    '/geoatm'         : modules.atm_feature.geodata_stop,
                    '/searchatm'      : modules.atm_feature.search_line,
                    '/treni'          : modules.viaggiatreno.timetable2stations,
                    '/infotreno'      : modules.viaggiatreno.send_delay,
                    '/covid'          : modules.covid.covid_cases,
                    '/vaccine'        : modules.covid.check_vaccine_function,
                    '/poll'           : usys.poll_function,
                    '/weather'        : modules.weather.get_weather,
                    '/forecastoday'   : modules.weather.get_today_forecasts,
                    '/forecastfuture' : modules.weather.get_future_forecasts,
                    '/weathermap'     : modules.weather.wttrin_map,
                    '/weathersat'     : modules.weather.sat24_map,
                    '/reminder'       : modules.reminder.set_reminder,
                    '/urban'          : modules.urban.urban_search,
                    '/mystat'         : udb.show_stats,
                    '/tper'           : modules.tper.send_tper_stop,
                    '/tpershop'       : modules.tper.get_tper_edicola,
                    '/trivial'        : modules.trivial.send_question,
                    '/mytscore'       : modules.trivial.get_personal_score,
                    '/globaltscore'   : modules.trivial.get_global_score,
                    '/infopista'      : modules.pistekart.get_info_pista,
                    '/piste'          : modules.pistekart.get_piste_region,
                    '/eq'             : modules.ingv.get_eq_data,
                    '/ral'            : modules.ral.ral_calc,
                    '/math'           : modules.math.calculate,
                    '/cat'            : modules.animals.get_cat, 
                    '/dog'            : modules.animals.get_dog, 
                    '/fox'            : modules.animals.get_fox, 
                    '/rabbit'         : modules.animals.get_rabbit, 
                    '/bird'           : modules.animals.get_bird, 
                    '/yt'             : modules.videodl.youtube_dl,
                    '/latex'          : modules.latex.get_latex,
                    '/passport'       : modules.passport.get_passport_info,
                    '/extremeforecast': modules.weatherextreme.get_extreme_forecast,
                    '/apod'           : modules.space.get_daily_apod,
                    '/bggsearch'      : modules.bgg.search_board_game,
                    '/bgg'            : modules.bgg.get_board_game_data,
                    '/flight'         : modules.flight.get_flight_info,
                    '/airline'        : modules.flight.get_airlines_info,
                    '/joke'           : modules.jokes.get_random_joke,
                    '/helprob'        : usys.help}

#Dizionario con l'elenco dei comandi admin
dictionary_admin = {'/getmessage'     : usys.get_message,
                    '/playlotto'      : usys.play_lotto,
                    '/ai'             : modules.openai.openai_completion,
                    '/amount'         : udb.show_personal_amount,
                    '/aimg'           : modules.openai.openai_dalle,
                    '/pingrob'        : usys.ping}

#Dizionario con l'elenco dei comandi superadmin
dictionary_super = {'/setrobuser'     : udb.set_user,
                    '/delrobuser'     : udb.del_user,
                    '/updaterobuser'  : udb.update_user,
                    '/listrobuser'    : udb.list_user,
                    '/allrobuser'     : udb.all_user,
                    '/setrobadmin'    : udb.set_admin,
                    '/delrobadmin'    : udb.del_admin,
                    '/setgroup'       : udb.set_group,
                    '/listgroup'      : udb.list_group,
                    '/delgroup'       : udb.del_group,
                    '/updategroup'    : udb.update_group,
                    '/allamounts'     : udb.show_all_amounts,
                    '/setamount'      : udb.set_amount,
                    '/updatestat'     : udb.force_update_stats,
                    '/restart'        : usys.restart,
                    '/say'            : usys.send_user,
                    '/delstat'        : udb.force_delete_stats}

auth_command = ["/trivial"]

"""
Questa funzione prende come argomento il match e la richiesta dal main e dirotta la richiesta sul file dedicato a quel comando
"""
def fetch_command(match,query,client,message):
    #controllo sui comandi autorizzati solo in determinate chat
    if udb.check_group_command(match,message) and match in auth_command:
        return ugc.sendMessage(client,message,"__Comando non autorizzato in questa chat.\nContatta @MasterCruelty per informazioni.__")
    else:
        udb.update_stats(ugc.get_id_user(message),match)
        dictionary[match](query,client,message)
"""
Analogamente a fetch_command ma per i comandi esclusivi degli utenti admin
"""
def fetch_admin_command(match,query,client,message):
    #system functions
    udb.update_stats(ugc.get_id_user(message),match)
    dictionary_admin[match](query,client,message)

"""
Analogamente a fetch_command ma per i comandi esclusivi del super admin
"""
def fetch_super_command(match,query,client,message):
    #db functions
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
    except IndexError:
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
#prelevo id super admin dal file di configurazione
config = ugc.get_config_file("config.json")
id_super_admin = config["id_super_admin"].split(";")[0]

@Client.on_message()
def visualizza(chat,nome_chat,utente,nome_utente,username,messaggio,client):
    result = "id utente: " + str(utente) + "\nnome utente: " + nome_utente + "\nusername: " + username
    print("id_utente: " + str(utente) + "\nnome_utente: " + nome_utente + "\nusername: " + username)
    if str(chat):
        result += "\nchat id: " + str(chat) + "\nnome chat: " + str(nome_chat) + "\nmessaggio: " + messaggio
        print("chat_id: " + str(chat) + "\nnome_chat: " + str(nome_chat))
        print("messaggio: " + messaggio)
        print("**************************************************************************************")
    client.send_message(id_super_admin,result)
