from utils.get_config import sendMessage,get_chat,get_id_msg,sendPhoto
from pyrogram import Client,filters,errors
import re
import requests
from bs4 import BeautifulSoup
import warnings

"""
    Restituisce dati sugli ultimi 5 terremoti avvenuti con scala maggiore di 2 da INGV
"""
def get_eq_data(query,client,message):
    resp = requests.get("https://webservices.ingv.it/fdsnws/event/1/query?&minmag=2")
    content = resp.content
    zuppa = BeautifulSoup(content,'xml')
    events = zuppa.find_all("event")
    result = ""
    text_message = ""
    check = False
    i = 0
    for item in events:
        if i > 5:
            break
        place = "**" + item.description.get_text() +"**"
        magnitude = "Magnitudo: __" + item.magnitude.mag.get_text().split("\n")[1] + "__\n"
        split_time = item.origin.time.value.text.split("T")
        origin_time = "__Avvenuto in questo orario: " + split_time[0] + " alle " + split_time[1]  + "__\n"
        lat = float(item.origin.latitude.value.text)
        lon = float(item.origin.longitude.value.text)
        event_id = item["publicID"].split("eventId=")[1]
        url_image = "https://shakemap.rm.ingv.it/shake4/data/" + event_id + "/current/products/intensity.jpg"
        warnings.filterwarnings("ignore",category=requests.packages.urllib3.exceptions.InsecureRequestWarning)
        image_resp = requests.get(url_image,timeout=5,verify=False)
        result += place + magnitude + origin_time
        if "404" in image_resp.text:
            check = True
            text_message += place + magnitude + origin_time + "\n\n"
            result = ""
        else:
            check = True
            try:
                sendPhoto(client,message,url_image,result)
            except errors.exceptions.bad_request_400.MediaEmpty:
                i = i + 1
                continue
            result = ""
        i = i + 1
    if check == False:
        return sendMessage(client,message,"__Nessun dato trovato__")
    else:
        return sendMessage(client,message,"__Ecco gli ultimi terremoti avvenuti.__\n" + text_message)
