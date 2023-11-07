from utils.get_config import sendMessage,sendPhoto
from pyrogram import Client,errors
from FlightRadar24 import FlightRadar24API
import flightradar24
import datetime

"""
    Restituisce informazioni relative al volo richiesto dato il numero di volo
"""
def get_flight_info(query,client,message):
    fr = flightradar24.Api()
    flight = fr.get_flight(query)
    flight_info = ""
    flight_data = []
    #Getting only flight with estimated arrive or departure
    for i in range(len(flight['result']['response']['data'])):
        if "estimated" in flight['result']['response']['data'][i]['status']['generic']['status']['text']:
            flight_data.append(flight['result']['response']['data'][i])
    if flight_data == []:
        return sendMessage(client,message,"__Non risulta nessun volo in atto con quel numero al momento.__")
    
    #building result string for every flight matching my policy(estimated)
    for i in range(len(flight_data)):
        flight_number = flight_data[i]['identification']['number']['default']
        aircraft_model = flight_data[i]['aircraft']['model']['text']
        origin = flight_data[i]['airport']['origin']['name'] + "(<code>" + flight_data[i]['airport']['origin']['code']['iata'] + "</code>)"
        destination = flight_data[i]['airport']['destination']['name'] + "(<code>" + flight_data[i]['airport']['destination']['code']['iata'] + "</code>)"
        scheduled_departure = flight_data[i]['time']['scheduled']['departure']
        scheduled_departure = datetime.datetime.utcfromtimestamp(scheduled_departure)
        scheduled_arrival = flight_data[i]['time']['scheduled']['arrival']
        scheduled_arrival = datetime.datetime.utcfromtimestamp(scheduled_arrival)
        scheduled_updated = flight_data[i]['time']['other']['updated']
        scheduled_updated = datetime.datetime.utcfromtimestamp(scheduled_updated)
        flight_status = flight_data[i]['status']['text']
        flight_airline = flight_data[i]['airline']['name']
        duration = scheduled_arrival - scheduled_departure
        hours, seconds = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        
        formatted_duration = f"{hours}:{minutes}"

        img = flight['result']['response']['aircraftImages'][i]['images']['large'][0]['src']

        flight_info = f"__Flight__: **{flight_number}**\n"
        flight_info += f"__Airline__: **{flight_airline}**\n"
        flight_info += f"__Aircraft model__: **{aircraft_model}**\n"
        flight_info += f"__Origin__: **{origin}**\n"
        flight_info += f"__Destination__: **{destination}**\n"
        flight_info += f"__Scheduled Departure__: **{scheduled_departure}**\n"
        flight_info += f"__Scheduled Arrival__: **{scheduled_arrival}**\n"
        flight_info += f"__Updated arrival__: **{scheduled_updated}**\n"
        flight_info += "__Scheduled duration__: **" + formatted_duration + "**\n"
        flight_info += f"Flight Status: **{flight_status}**\n"
        sendPhoto(client,message,img,flight_info)

"""
    Restituisce i dati principali di una compagnia aerea data la parola chiave
"""
def get_airlines_info(query,client,message):
    query = query.title()
    fr = FlightRadar24API()
    airlines = fr.get_airlines()
    result = ""
    #I look for every airline matching my request
    for i in range(len(airlines)):
        if query in airlines[i]['Name']:
            result += "**Nome**: <code>" + airlines[i]['Name'] + "</code>\n**IATA**: <code>" + airlines[i]['Code'] + "</code>\n**ICAO**: <code>" + airlines[i]['ICAO'] + "</code>\n"
    if result != "": 
        sendMessage(client,message,result)
    else:
        sendMessage(client,message,"__Nessuna compagnia aerea trovata.__")

"""
    Restituisce informazioni sull'aereporto selezionato dato il codice IATA
"""
def get_airport_info(query,client,message):
    fr = FlightRadar24API()
    try:
        airport = fr.get_airport_details(query.upper())
        airlines = airport["airlines"]
        airport = airport["airport"]["pluginData"]
    except KeyError:
        return sendMessage(client,message,"__Errore nella richiesta dell'aereoporto.__")
    #building different strings and collecting airport data
    name = "__" + str(airport["details"]["name"]) + "__ (<code>" + str(airport["details"]["code"]["iata"]) + "</code>)\n"
    rating = "**Media**: __" + str(airport["flightdiary"]["ratings"]["avg"]) + "__\n**Totale voti**: __" + str(airport["flightdiary"]["ratings"]["total"]) + "__\n" 
    aircrafts_ground = "**Totale aerei a terra**: __" + str(airport["aircraftCount"]["ground"]) + "__\n"
    runways = airport["runways"]
    tot_runways = str(len(runways))
    runways_data = "\n**Totale Piste:** __" + tot_runways + "__\n"
    for item in runways:
        runways_data += "**Nome**: __" + str(item["name"]) + "__\n**Lunghezza**: __" +  str(item["length"]["m"]) + " metri.__\n**Superficie**: __" + str(item["surface"]["name"]) + "__\n" 
    airlines_data = "\n**Compagnie aeree operanti**:\n"
    try:
        for airline_code, airline_data in airlines["codeshare"].items():
            airlines_data += "<code>" + str(airline_data["name"]) + "</code>; " 
    except:
        airlines_data += "__None__"
    
    #collecting data about arrival and departure flights
    arrivals = airport["schedule"]["arrivals"]["data"]
    arrivals_data = "\n**Numeri voli in arrivo**:\n"
    for i in range(len(arrivals)):
        arrivals_data += "<code>" + str(arrivals[i]["flight"]["identification"]["number"]["default"]) + "</code>; "
    departures = airport["schedule"]["departures"]["data"]
    departures_data = "\n**Numeri voli in partenza**:\n"
    for i in range(len(departures)):
        departures_data += "<code>" + str(departures[i]["flight"]["identification"]["number"]["default"]) + "</code>; "

    img = airport["details"]["airportImages"]["large"][0]["src"]
    result = name + rating + aircrafts_ground + runways_data + airlines_data + arrivals_data + departures_data 
    try:
        return sendPhoto(client,message,img,result)
    except:
        sendPhoto(client,message,img,name + rating + aircrafts_ground + runways_data)
        return sendMessage(client,message,airlines_data + arrivals_data + departures_data)

