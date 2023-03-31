from utils.get_config import sendMessage,sendPhoto
from pyrogram import Client,errors
import requests
from bs4 import BeautifulSoup
import re

"""
    scapring di passportindex per ottenere info principali sulla potenza di un passaporto
"""
def get_passport_info(query,client,message):
    query = query.replace(" ","-")
    url = "https://passportindex.org/passport/" + query.lower() + "/"
    resp = requests.get(url)
    zuppa = BeautifulSoup(resp.text,"html.parser")
    tags = zuppa.find_all("div",attrs={"class":"hidden-sm hidden-lg hidden-md col-xs-8 text-left psprt-dashboard-info"})
    result = [tag.getText() for tag in tags if tag.getText() != ""]
    #estrapolo la stringa dal result
    result = ''.join(result).strip()
    #creo il pattern e il match per la regex per formattare la stringa
    pattern = r'(\w[\w\s-]+?)\s+(\d+[\d\s%]*)'
    matches = re.findall(pattern, result)
    final_string = '\n'.join(['{}: {}'.format(key.strip(), value.strip()) for key, value in matches])
    final_string = final_string.replace("Visa-free","Visa-free: ")
    imgtag = zuppa.find("div",attrs={"class": "psprt-dashboard-cover"}).find('img')
    img_url = imgtag['src']
    return sendPhoto(client,message,img_url,final_string)
