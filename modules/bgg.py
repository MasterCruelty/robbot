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
    data = requests.get(url)
    regex = re.findall('description>([^<]*)',data.text)
    title = regex[0]
    regex = re.findall('description>([^<]*)',data.text)
    description = regex[0]
    result = "**" + data[0] + "**\n" + "__" + data[1] + "__"
    return sendMessage(client,message,result)


def search_board_game(query,client,message):
        url_search = "https://boardgamegeek.com/xmlapi/search?search=halo fleet battles the fall of reach"
