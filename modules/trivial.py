from utils.get_config import sendMessage,get_chat,get_id_msg 
from pyrogram import Client,errors
import requests
import json

global token

categorie = {"General Knowledge"     :9,
             "Books"                 :10,
             "Film"                  :11,
             "Music"                 :12,
             "Musical & Theatres"    :13,
             "Television"            :14,
             "Video Games"           :15,
             "Board Games"           :16,
             "Science & Nature"      :17,
             "Science & Computers"   :18,
             "Science & Mathematics" :19,
             "Mythology"             :20,
             "Sports"                :21,
             "Geography"             :22,
             "History"               :23,
             "Politics"              :24,
             "Art"                   :25,
             "Celebrities"           :26,
             "Animals"               :27,
             "Vehicles"              :28,
             "Comics"                :29,
             "Science & Gadgets"     :30,
             "Japanese Anime & Manga":31,
             "Cartoon & Animations"  :32}


"""
    Chiamata per la creazione di un token che garantisce l'unicità delle domande fetchate da opentb.com
    Il token ha una vita di 6 ore se inattivo ininterrottamente.
    Una volta esaurito, va resettato e generato di nuovo.
"""
def create_token():
    global token
    url = "https://opentdb.com/api_token.php?command=request"
    resp = requests.get(url)
    data = json.loads(resp.text)
    if data["response_code"] == 0:
        token = data["token"]
    else:
        return "__Errore durante la creazione token.__"
    return token

"""
    Chiamata per il reset del token nel caso in cui sia stato esaurito completamente.
"""
def reset_token():
    global token
    url = "https://opentb.com/api_token.php?command=reset&token=" + token
    resp = requests.get(url)
    data = json.loads(resp.text)
    if data["response_code"] == 0:
        token = data["token"]
    else:
        return "__Errore durante reset token.__"
    return token
