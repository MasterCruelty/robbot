from utils.get_config import sendMessage,get_chat,get_id_msg 
from pyrogram import Client,filters,errors
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from pyrogram.handlers import CallbackQueryHandler
import requests
import json
import datetime
import time



"""
    Restituisce il codice stazione della stazione richiesta oppure null se non trovata
    primo tentativo con api viaggiatreno, secondo tentativo con api frecce
"""
def get_station_code(name):
    if name.startswith(" "):
        name = name[1:]
    url = "http://www.viaggiatreno.it/infomobilita/resteasy/viaggiatreno/cercaStazione/" + name
    resp = requests.get(url)
    try:
        data = json.loads(resp.text)
    except json.decoder.JSONDecodeError:
        #provo con le api frecce se viaggiatreno non trova la stazione
        url = "https://lefrecce.it/Channels.Website.BFF.WEB/website/locations/search?name=" + name + "&limit=10" 
        resp = requests.get(url)
        try:
            data = json.loads(resp.text)
        except json.decoder.JSONDecoreError:
            return None
        for item in data:
            if name.title() in item["displayName"] or name.title()[5:] in item["displayName"]:
                return str(item["id"]).replace("83000","")
            else:
                return None
    #vedo se tra i risultati trovati c'è il nome della stazione cercato e restituisco il suo codice stazione
    for item in data:
        if name.upper() in item["nomeLungo"] or name.title() in item["nomeBreve"]:
            return item["id"]
        else:
            return None 



"""
    tolgo la S e gli zeri iniziali per adattare il codice stazione ad alcune chiamate
"""
def format_station_code(station):
    station = station.replace("S","")
    #rimuovo il carattere S e i primi zeri che compaiono altrimenti non va a buon fine la richiesta
    while True:
        if station.startswith("0"):
            station = station[1:]
        else:
            break
    return station

"""
    Restituisce i dati delle partenze di treni che vanno da una stazione A a una stazione B con gli orari e altre info
"""
global pages
global k

@Client.on_message()
def timetable2stations(query,client,message):
    global pages
    global k
    price = False
    #controllo se richiesto il prezzo e preparo la funzione dedicata ai prezzi
    if "-price" in query:
        price = True
        query = query.replace("-price ","")
    splitted = query.split(",")
    try:
        from_station = get_station_code(splitted[0])
        to_station = get_station_code(splitted[1]) #da pos 1 perché c'è uno spazio
    except IndexError:
        return sendMessage(client,message,"__Errore formato.\nProva /helprob trenitalia__")
    #controllo se richiesta una data specifica altrimenti metto quella odierna
    if len(splitted) < 3:
        now = str(datetime.datetime.now())
        date_time = now.replace(" ","T")
    else:
        date_time = splitted[2] + "T00:00:00"
    #controllo opzione prezzi ed eseguo la funzione dedicata che usa le api frecce con codici stazione e data già calcolati.
    if price:
        return timetable_with_price(client,message,from_station,to_station,date_time)
    #formatto i codici stazione per essere in regola per la chiamata dopo
    try:
        from_station = format_station_code(from_station)
        to_station = format_station_code(to_station)
    except AttributeError:
        return sendMessage(client,message,"__Stazione non trovata__")

    #preparo l'url per la chiamata, i parametri sono pronti
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
            result += "__Questa soluzione presenta dei cambi__\n\n"
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
    print("Giro pagina in /treni")
    global k
    if k < len(pages)-1:
        k = k + 1
        kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("Prossimi treni",callback_data="PROSSIMI")]])
        message.edit_message_text(pages[k],reply_markup=kb)
    else:
        message.edit_message_text("__Fine__")

"""
    Restituisce info sui prezzi della tratta richiesta nel giorno richiesto(oggi se omesso)
"""
global pages2
global k2
def timetable_with_price(client,message,from_station,to_station,date_time):
    global pages2
    global k2
    #api frecce
    url ="https://www.lefrecce.it/Channels.Website.BFF.WEB/website/ticket/solutions"
    #headers aggiuntivi per sicurezza
    headers = { "Origin": "https://www.lefrecce.it",
                "Referer":"https://www.lefrecce.it",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0;Win64;x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
              }
    #formatto i codici stazione e poi aggiungo prefisso 83000 per api frecce ai codici stazione
    from_station = format_station_code(from_station)
    to_station = format_station_code(to_station)

    from_station = int("83000" + str(from_station))
    to_station = int("83000" + str(to_station))
    date_time += "+01:00"
    
    #preparo il payload per la post
    data = { "departureLocationId": from_station,
             "arrivalLocationId":   to_station,
             "departureTime":       date_time.replace(" ",""),
             "adults": 1,
             "children": 0,
             "criteria": {
                 "frecceOnly": False,
                 "regionalOnly": False,
                 "noChanges": False,
                 "order": "DEPARTURE_DATE",
                 "limit": 15,
                 "offset": 0
            },
            "advancedSearchRequest": {
                "bestFare": False
            }
        }
    #faccio la richiesta
    resp = requests.post(url,json=data,headers=headers)

    data = json.loads(resp.text)
    data = data["solutions"]

    #estrapolo i dati che ci interessano dal json e inizializzo la globale pags2
    pages2 = []
    for item in data:
        day = item["solution"]["departureTime"].split("T")[0]
        depart_time = str(item["solution"]["departureTime"].split("T")[1])[0:5]
        arrival_time = str(item["solution"]["arrivalTime"].split("T")[1])[0:5]
        journey_time = "(" + depart_time + "-" + arrival_time + ")"
        durata = "**Durata: " + item["solution"]["duration"] + "**"
        vendibile = "Vendibile" if item["solution"]["status"] == "SALEABLE" else "Non vendibile"
        tratta = item["solution"]["origin"] + "==>" + item["solution"]["destination"]
        try:
            prezzo = str( "%0.2f" % item["solution"]["price"]["amount"])
            prezzo += item["solution"]["price"]["currency"]
        except TypeError:
            prezzo = "Non disponibile"

        result = "**" + day + "**\n\n"
        if len(item["solution"]["trains"]) > 1:
            result += "__Questa soluzione presenta dei cambi.__\n**Per vedere quali**, digita <code>/treni " + item["solution"]["origin"] + ", " + item["solution"]["destination"] + "," + day + "T" + depart_time + ":00" +  "</code>\n__È sufficiente toccare e incollare.__"
        result += "\n**" + tratta + journey_time + "**\n\n__Prezzo: " + prezzo + "__"
        result += "\n**" + durata + "**\n__Stato: " + vendibile + "__" 
        pages2.append(result)

    #build keyboard
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("Prossimi treni",callback_data="PROSSIMI_prezzi")]])


    #add handler
    client.add_handler(CallbackQueryHandler(callback=press_button_price,filters=filters.regex("PROSSIMI_prezzi")))
    k2 = 0
    try:
        client.send_message(get_chat(message),pages2[k2],reply_markup=kb,reply_to_message_id=get_id_msg(message))
    except IndexError:
        return sendMessage(client,message,"__Errore formato.\nProva /helprob treni__")



"""
    funzione callback per il bottone "prossimi treni" che fa visualizzare la pagina successiva
"""
@Client.on_callback_query(filters = filters.regex("PROSSIMI_prezzi"))
def press_button_price(client,message):
    print("Giro pagina in /treni -price")
    global k2
    if k2 < len(pages2)-1:
        k2 = k2 + 1
        kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("Prossimi treni",callback_data="PROSSIMI_prezzi")]])
        message.edit_message_text(pages2[k2],reply_markup=kb)
    else:
        message.edit_message_text("__Fine__")

"""
    Restituisce la stazione di partenza del treno indicato(non utilizzata al momento)
"""
def departStation_train(train_number):
    url = "http://www.viaggiatreno.it/infomobilita/resteasy/viaggiatreno/cercaNumeroTreno/" + train_number
    resp = requests.get(url)
    if resp.text == '':
        return sendMessage(client,message,"__Treno non trovato__")
    data = json.loads(resp.text)
    return data["codLocOrig"]


"""
    Restituisce informazioni riguardo l'eventuale ritardo accumulato sul treno richiesto
"""
def get_delay(query,client,message):
    #calcolo il codice stazione di partenza rispetto al numero del treno
    station_code = departStation_train(query)
    train_number = query 

    timestamp_url = "http://www.viaggiatreno.it/infomobilita/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/" + train_number
    resp = requests.get(timestamp_url)
    splitted = resp.text.split("\n")
    if len(splitted) > 1 and len(splitted[1]) > 2:
        s = splitted[1]
    else:
        s = splitted[0]
    s = s.split("-")
    timestamp = ""
    for i in range(len(s)):
        if len(s[i]) == 13:
            timestamp = s[i]
    #modifico url e faccio chiamata su un'altra rotta per ottenere l'ultimo rilevamento
    url = "http://www.viaggiatreno.it/infomobilita/resteasy/viaggiatreno/andamentoTreno/" + station_code + "/" + train_number + "/" + timestamp
    resp = requests.get(url)
    try:
        data = json.loads(resp.text)
    except json.decoder.JSONDecoreError:
        return sendMessage(client,message,"__Treno non trovato__")

       
    #estrapolo i dati dal json
    info_train = "Treno: __" + data["categoria"] + " " + str(data["numeroTreno"]) + "(" + data["compTipologiaTreno"] + ")__"
    route = "Tratta: __" + data["origine"].title() + "==>" + data["destinazione"].title() + "__"
    #controllo se il treno è in viaggio o è fermo in stazione
    if data["inStazione"] ==  False:
        in_station = "**Risulta in viaggio**"
    else:
        in_station = "**Risulta fermo in stazione**"
    #Ritardo sul treno
    delay = "Il treno viaggia __" + data["compRitardoAndamento"][0] + "__"
    duration = data["compDurata"]
    expected_depart = "Partenza prevista da " + data["origine"].title() + ": __" + data["compOrarioPartenzaZero"] + "__"
    real_depart = "Partenza effettiva da " + data["origine"].title() + ": __" + data["compOrarioPartenzaZeroEffettivo"] + "__"
    expected_arrival = "Arrivo previsto a " + data["destinazione"].title() + ": __" + data["compOrarioArrivoZero"] + "__"
    real_arrival = "Arrivo effettivo a " + data["destinazione"].title() + ": __" + data["compOrarioArrivoZeroEffettivo"] + "__"
    
    #ultimo rilevamento
    last_detection = data["stazioneUltimoRilevamento"].title()
    last_time_detection = data["compOraUltimoRilevamento"]
    
    #Inizio a cosstruire la stringa da restituire
    result = info_train + "\n" + route + "\nStato: " + in_station + "\n" + delay + "\nDurata prevista: **" + duration + "**\n" + expected_depart + "\n" + real_depart + "\n" + expected_arrival + "\n" + real_arrival + "\n"

    #aggiungo info alla stringa costruita prima
    result += "\nOra ultimo rilevamento: __" + str(last_time_detection) + "__"
    result += "\nStazione ultimo rilevamento: __" + last_detection + "__"
    
    #elenco fermate
    fermate = data["fermate"]
    stops = "Fermate : **"
    for stop in fermate:
        stops += stop["stazione"].title() + "=>"
    stops += "**"
    result += "\n\n" + stops
    return result

"""
    Invia il messaggio con i dati relativi al treno richiesto(dati presi da get_delay() qua sopra
"""
@Client.on_message()
def send_delay(query,client,message):
    #recupero la stringa
    try:
        result = get_delay(query,client,message)
    except NameError:
        return sendMessage(client,message,"__Errore generico.__")

    #build keyboard
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("Refresh",callback_data="REFRESH;"+str(query))]])

    #add handler
    client.add_handler(CallbackQueryHandler(callback=press_button_refresh,filters=filters.regex("REFRESH;"+str(query))))
    client.send_message(get_chat(message),result,reply_markup=kb,reply_to_message_id=get_id_msg(message))

"""
    Aggiorna lo stato del treno richiesto in precedenza
"""
@Client.on_callback_query()
def press_button_refresh(client,message):
    cb = message.data.split(";")
    query = cb[1]
    print("Premuto bottone /infotreno con richiesta: " + str(query))
    #build keyboard
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("Refresh",callback_data="REFRESH;"+str(query))]])
    #edit message
    try:
        message.edit_message_text(get_delay(query,client,message),reply_markup=kb)
    except errors.exceptions.bad_request_400.MessageNotModified:
        message.edit_message_text(get_delay(query,client,message) + "\n__Nessun aggiornamento per ora__", reply_markup=kb)
        time.sleep(5)




