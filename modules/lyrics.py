import urllib.request
from bs4 import BeautifulSoup
from utils.get_config import sendMessage


def execute_lyrics(query,client,message):
    parametri = query.split(",")
    if len(parametri) > 1:
        result = get_lyrics_formated(parametri[0],parametri[1])
    else:
        result = search_songs(parametri[0])
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
dato l'artista, restituisce tutti i suoi brani
"""
def search_songs(artista):
    artista = format_input(artista)
    url = "https://azlyrics.com/" + artista[0] + "/" + artista + ".html"
    page = handle_except(url)
    if "404" in str(page):
        return page
    zuppa = BeautifulSoup(page,"html.parser")
    results_tags = zuppa.find_all("div",attrs={"class": None,"id": "listAlbum"})
    results = [tag.getText() for tag in results_tags]
    results = "__" + "\n".join(results) + "__"
    result = ""
    for word in results.split("\n"):
        if word.startswith("album"):
            word = "++++++++++++++++++++++\n**" + word + "**" + "\n"
        result += word + "\n"
    return result
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

