from utils.get_config import sendMessage,sendPhoto
from pyrogram import Client,errors
import requests

"""
    Restituisce il LaTeX compilato tramite api pubblica
"""
def get_latex(query,client,message):
    if " " in query:
        query = query.replace(" ","%20")
    url = "https://latex.codecogs.com/png.image?\dpi{200}" + query
    return sendPhoto(client,message,url,"__Result LaTeX__")