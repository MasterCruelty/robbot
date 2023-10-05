from utils.get_config import sendPhoto,sendMessage,get_chat,get_id_msg 
#from pyrogram import Client,filters,errors
#from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
#from pyrogram.handlers import CallbackQueryHandler
import re
import requests
from xml.etree import cElementTree as ET


"""
   Restituisce i dati del gioco da tavolo richiesto.
"""
def get_board_game_data(query,client,message):
    url_info = "https://boardgamegeek.com/xmlapi2/thing?id=" + query
    data = requests.get(url_info)

    root = ET.fromstring(data.text)
    result = ""
    categories = ""
    publisher = ""
    #prelevo titolo del gioco
    title = root.find(".//name[@type='primary']").get('value')
    #prelevo il link dell'immagine
    img_url = root.find(".//image").text
    #prelevo la descrizione
    descr = root.find(".//description").text
    #prelevo l'anno di pubblicazione
    year = root.find(".//yearpublished").get('value')
    #prelevo numero minimo e massimo di giocatori
    minplayer = root.find(".//minplayers").get('value')
    maxplayer = root.find(".//maxplayers").get('value')
    #prelevo durata di gioco 
    playingtime = root.find(".//playingtime").get('value')
    minplayingtime = root.find(".//minplaytime").get('value')
    maxplayingtime = root.find(".//maxplaytime").get('value')
    #cerco publisher e categorie del gioco
    #todo: boardgamemechanic, boardgameexpansion, boardgameaccessory,boardgameintegration
    root = ET.fromstring(data.text)
    for link in root.iter('link'):
        link_type = link.get('type')
        if link_type == 'boardgamepublisher':
            publisher = link.get('value')
        if link_type == 'boardgamecategory':
            categories += link.get('value') + ", "
    caption = "**" + title + "**\n\nAnno di pubblicazione:__ " + year + "\n__Publisher:__ " + publisher + "__\nCategorie:__ " + categories + "__\n"
    result += "__" + descr + "__\n\nNumero minimo di giocatori: __ " + minplayer + "__\n"    
    result += "**Numero massimo di giocatori**:__ " + maxplayer + "__\n**Tempo di gioco**:__ " + playingtime + " minuti__\n**Minimo**:__ " + minplayingtime + " minuti__\n"
    result += "**Massimo**:__ " + maxplayingtime + " minuti__"
    sendPhoto(client,message,img_url,caption)
    return sendMessage(client,message,result)

"""
    Restituisce i risultati della ricerca per la keyword inserita
"""
def search_board_game(query,client,message):
    url_search = "https://boardgamegeek.com/xmlapi/search?search=" + query
    data = requests.get(url_search)
    pattern = re.compile(r'<boardgame objectid="(\d+)">\s*<name.*?>(.*?)</name>\s*<yearpublished>(\d+)</yearpublished>', re.DOTALL)
    matches = pattern.findall(data.text)
    result = ""
    for match in matches:
        object_id, name, year_published = match
        result += f"**Titolo**: __{name}__\n**Anno**: __{year_published}__\n**ID**: <code>{object_id}</code>\n" + "\n"
    return sendMessage(client,message,result)


