from utils.get_config import sendMessage,get_chat,get_id_msg,sendPhoto
from pyrogram import Client,errors
import requests
import json

"""
    It send the daily pic from nasa APOD(Astronomy Picture of the Day)
"""
def get_daily_apod(query,client,message):
    url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
    resp = requests.get(url)
    data = json.loads(resp.text)
    title = data['title']
    caption = "**" + title + "**\n__" + data['explanation'] + "__"
    pic = data['url']
    try:
        return sendPhoto(client,message,pic,caption)
    except:
        caption = "**La descrizione è più lunga rispetto al limite di un messaggio Telegram.**\n__Puoi leggerla qui:__ https://apod.nasa.gov"  
        return sendPhoto(client,message,pic,caption)
    
