import urllib.request
from bs4 import BeautifulSoup
from utils.get_config import get_chat, get_id_msg,sendMessage
from pyrogram import Client,filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from pyrogram.handlers import CallbackQueryHandler


def execute_lyrics(query,client,message):
    parametri = query.split(",")
    if len(parametri) > 1:
        result = get_lyrics_formated(parametri[0],parametri[1])
    else:
        return search_songs(client,message,parametri[0])
    return sendMessage(client,message,result)

"""
Questa funzione, dati artista e canzone, effettua una richiesta http a azlyrics.com e filtrando i tag con una bellissima zuppa,
ci restituisce le lyrics della canzone desiderata(se esiste sul sito)
"""
def get_lyrics_formated(artista,canzone):
    artista = format_input(artista)
    canzone = format_input(canzone)
    url = "https://azlyrics.com/lyrics/" + artista + "/" + canzone + ".html"
    page = handle_except(url) 
    if "404" in str(page):
        return page
    zuppa = BeautifulSoup(page,"html.parser")
    lyrics_tags = zuppa.find_all("div",attrs= {"class": None, "id": None})
    lyrics = [tag.getText() for tag in lyrics_tags]
    result = "\n".join(lyrics)
    return result

"""
dato l'artista, restituisce tutti i suoi brani.
Le variabili globali pages e k sono usate per gestire i dati con la funzione callback per il bottone inline.
"""
global pages
global k

@Client.on_message()
def search_songs(client,message,artista):
    global pages
    global k
    artista_formated = format_input(artista)
    url = "https://azlyrics.com/" + artista_formated[0] + "/" + artista_formated + ".html"
    page = handle_except(url)
    if "404" in str(page):
        return page
    zuppa = BeautifulSoup(page,"html.parser")
    results_tags = zuppa.find_all("div",attrs={"class": None,"id": "listAlbum"})
    results = [tag.getText() for tag in results_tags]
    results = "\n".join(results)
    album = ""

    
    #recupero i dati e poi popolo la globale pages
    for track in results.split("\n"):
        if track.startswith("album"):
            track = "{\n**" + track + "**" + "\n"
        album += track + "\n"
    
    #formatto bene pages
    pages = album.split("{")
    pages.pop(0)


    #costruisco la tastiera e definisco il bottone
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("Prossimo Album",callback_data="next_album")]])

    #aggiungo l'handler callbackquery per far catturare l'evento del bottone premuto alla funzione press_next_album
    client.add_handler(CallbackQueryHandler(callback=press_next_album,filters=filters.regex("next_album")))

    #mando il messaggio con la prima pagina
    k = 0
    client.send_message(get_chat(message),"__" + pages[k] + "__",reply_markup=kb,reply_to_message_id=get_id_msg(message))


"""
    Funzione che viene chiamata quando viene premuto il bottone costruito in search_songs
    utilizza le variabili globali definite a inizio file, pages è popolata in search_songs
    k viene incrementata in questa funzione per passare al prossimo elemento di pages.
"""
@Client.on_callback_query(filters.regex("next_album"))
def press_next_album(client,message):
    global k
    if k < len(pages)-1:
        k = k + 1
        kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("Prossimo Album",callback_data="next_album")]])
        message.edit_message_text("__" + pages[k] + "__",reply_markup=kb)
    else:
        message.edit_message_text("__Fine__")


"""
Questa funzione formatta una stringa in modo che sia pronta per essere usata in get_lyrics_formated
"""
def format_input(string):
    string = string.lower()
    string = string.replace(" ","")
    string = string.replace("'","")
    string = string.replace("-","")
    return string

"""
Questa funzione cattura ogni eventuale eccezione derivata da richiesta http errata a azlyrics.com 
Funzione ausiliaria di get_lyrics_formated
"""
def handle_except(url):
    try:
        page = urllib.request.urlopen(url)
    except:
        result = "404: page not found"
        return result
    return page

