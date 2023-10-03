from utils.get_config import sendMessage,get_chat,get_id_msg 
from pyrogram import Client,filters,errors
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from pyrogram.handlers import CallbackQueryHandler
import re
import requests


"""
   Restituisce i dati del gioco da tavolo richiesto.
"""
def get_board_game_data(query,client,message):
    url_info = "https://boardgamegeek.com/xmlapi2/thing?id=" + query
    data = requests.get(url_info)
    # Definisci un modello di regex per estrarre le informazioni desiderate
    pattern = re.compile(r'<boardgame objectid="(\d+)">\s*<yearpublished>(\d+)</yearpublished>\s*<minplayers>(\d+)</minplayers>\s*<maxplayers>(\d+)</maxplayers>\s*<name.*?>(.*?)</name>\s*<description>(.*?)</description>\s*<thumbnail>(.*?)</thumbnail>\s*<image>(.*?)</image>', re.DOTALL)

    # Trova tutte le corrispondenze nel testo XML utilizzando pattern
    matches = pattern.findall(data.text)
    sendMessage(client,message,matches)
    # Itera su ogni corrispondenza e stampa i risultati
    result = ""
    for match in matches:
        object_id, year_published, min_players, max_players, name, description, thumbnail, image = match
        result = f"Titolo: {name}\nAnno: {year_published}\nID: {object_id}\nMin giocatori: {min_players}\nMax giocatori: {max_players}\nDescrizione: {description}\nThumbnail: {thumbnail}\nImmagine: {image}\n"
    return sendMessage(client,message,result)

"""
    Restituisce i risultati della ricerca per la keyword inserita
"""
def search_board_game(query,client,message):
    url_search = "https://boardgamegeek.com/xmlapi/search?search=halo fleet battles the fall of reach"
    data = requests.get(url_search)
    pattern = re.compile(r'<boardgame objectid="(\d+)">\s*<name.*?>(.*?)</name>\s*<yearpublished>(\d+)</yearpublished>', re.DOTALL)
    matches = pattern.findall(data.text)
    for match in matches:
        object_id, name, year_published = match
        result = f"Titolo: {name}\nAnno: {year_published}\nID: {object_id}\n"
    return sendMessage(client,message,result)


