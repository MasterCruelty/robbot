from utils.get_config import sendMessage,get_chat,get_id_msg
from pyrogram import Client,filters,errors
from pyrogram.types import InputMediaPhoto
import requests
from bs4 import BeautifulSoup
import warnings
import io

"""
    Restituisce dati sugli ultimi 5 terremoti avvenuti con scala maggiore di 2 da INGV
"""
@Client.on_message()
def get_eq_data(query,client,message):
    resp = requests.get("https://webservices.ingv.it/fdsnws/event/1/query?&minmag=2")
    content = resp.content
    zuppa = BeautifulSoup(content,'xml')
    events = zuppa.find_all("event")
    text_message = ""
    i = 0
    media = []
    for item in events:
        #mostro solo gli ultimi 5 terremoti, quindi i primi 5 della lista
        if i > 5:
            break
        place = "**" + item.description.get_text().replace("region name","##############") +"**"
        magnitude = "Magnitudo: __" + item.magnitude.mag.get_text().split("\n")[1] + "__\n"
        split_time = item.origin.time.value.text.split("T")
        origin_time = "__Avvenuto in questo orario: " + split_time[0] + " alle " + split_time[1]  + "__"
        #lat = float(item.origin.latitude.value.text)
        #lon = float(item.origin.longitude.value.text)
        event_id = item["publicID"].split("eventId=")[1]
        url_image = "https://shakemap.rm.ingv.it/shake4/data/" + event_id + "/current/products/intensity.jpg"
        warnings.filterwarnings("ignore",category=requests.packages.urllib3.exceptions.InsecureRequestWarning)
        image_resp = requests.get(url_image,timeout=5,verify=False)
        if "404" in image_resp.text:
            text_message += place + magnitude + origin_time 
        else:
            #converto l'immagine in byte su ram perché send_media_group usa MTproto e non HTTP per inviare le immagini
            image_data = image_resp.content
            image_file = io.BytesIO(image_data)
            media.append(InputMediaPhoto(media=image_file,caption=place + magnitude + origin_time))
        i = i + 1
    try:
        client.send_media_group(get_chat(message),media=media)
    except errors.exceptions.bad_request_400.WebpageMediaEmpty:
        print("errore nell'invio delle immagini")
    sendMessage(client,message,"__Ecco i dati sugli terremoti avvenuti di cui non è presente un'immagine.\nSe clicchi sulle immagini disponibi potrai leggere i dettagli sulla magnitudo rispettiva.__\n" + text_message)
