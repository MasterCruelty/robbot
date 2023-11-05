from utils.get_config import sendMessage,sendPhoto
from pyrogram import Client,errors
import flightradar24
import datetime


def get_flight_info(query,client,message):
    fr = flightradar24.Api()
    flight = fr.get_flight(query)
    flight_info = ""
    flight_data = None
    for i in range(len(flight['result']['response']['data'])):
        if "Estimated" in flight['result']['response']['data'][i]['status']['text']:
            flight_data = flight['result']['response']['data'][i]
            break
    if flight_data == None:
        return sendMessage(client,message,"__Non risulta nessun volo in atto con quel numero al momento.__")

    flight_number = flight_data['identification']['number']['default']
    origin = flight_data['airport']['origin']['name']
    destination = flight_data['airport']['destination']['name']
    scheduled_departure = flight_data['time']['scheduled']['departure']
    scheduled_departure = datetime.datetime.utcfromtimestamp(scheduled_departure)
    scheduled_arrival = flight_data['time']['scheduled']['arrival']
    scheduled_arrival = datetime.datetime.utcfromtimestamp(scheduled_arrival)
    scheduled_updated = flight_data['time']['other']['updated']
    scheduled_updated = datetime.datetime.utcfromtimestamp(scheduled_updated)
    flight_status = flight_data['status']['text']
    flight_airline = flight_data['airline']['name']
    duration = scheduled_arrival - scheduled_departure
    hours, seconds = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    duration_real = flight_data['time']['other']['duration']
    
    formatted_duration = f"{hours}:{minutes}"

    img = flight['result']['response']['aircraftImages'][0]['images']['thumbnails'][0]['src']

    flight_info = f"__Flight__: **{flight_number}**\n"
    flight_info = f"__Airline__: **{flight_airline}**\n"
    flight_info += f"__Origin__: **{origin}**\n"
    flight_info += f"__Destination__: **{destination}**\n"
    flight_info += f"__Scheduled Departure__: **{scheduled_departure}**\n"
    flight_info += f"__Scheduled Arrival__: **{scheduled_arrival}**\n"
    flight_info += f"__Updated arrival__: **{scheduled_updated}**\n"
    flight_info += "__Scheduled duration__: **" + formatted_duration + "**\n"
    flight_info += f"Flight Status: **{flight_status}**\n"
    sendPhoto(client,message,img,flight_info)
