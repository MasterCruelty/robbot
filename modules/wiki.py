import wikipedia
import re
from pyrogram import Client
import utils.get_config
import utils.utility
from bs4 import BeautifulSoup



#Restituisce il parametro lingua
def get_lang(query):
    parole = query.split(" ")
    lingua = parole[0]
    return lingua
#restituisce le parole chiavi della ricerca eliminando la lingua
def get_keyword(query):
    words = query.split(" ")
    words.remove(words[0])
    search = ""
    for i in range(len(words)):
        search += words[i] + " "
    return search

#genero il link alla pagina wikipedia della pagina richiesta per saperne di più
def create_link(keyword,lang):
    page = wikipedia.page(keyword)
    keyword = page.title
    keyword = keyword.replace(" ","_")
    link = "<a href=\"https://"+lang+".wikipedia.org/wiki/"+keyword+"\">Guarda su Wikipedia</a>"
    return link

#Questa funzione esegue il comando wiki richiesto dall'app principale fetchato tramite la funzione in system.py
@Client.on_message()
def execute_wiki(query,client,message):
    if "/comune" in query:
        try:
            return comune(client,message)
        except:
            id_messaggio = utils.get_config.get_id_msg(message)
            client.edit_message_text(utils.get_config.get_chat(message),id_messaggio+1,"Operazione fallita")
            return
    lingua = get_lang(query)
    if len(lingua) > 3 or lingua == "all":
        return exec_wiki_ita(query,client,message)
    word = get_keyword(query)
    if " all " in query:
        return wikiall(word,client,message,lingua)
    if "random" in query:
        return wikirandom(1,False,client,message,lingua)
    else:
        return wiki(word,client,message,lingua)

#Esegue le funzioni wiki ma con lingua italiana come default
def exec_wiki_ita(query,client,message):
    if "all " in query:
        query = utils.utility.parser(query)
        return wikiall(query,client,message)
    if "random" in query:
        return wikirandom(1,False,client,message)
    else:
        return wiki(query,client,message)


#data la lingua e la parola chiave da cercare, restituisce una frase della voce trovata
def wiki(keyword,client,message,lang="it"):
   wikipedia.set_lang(lang)
   result = wikipedia.summary(keyword,sentences = 1) 
   result += "\n"+create_link(keyword,lang)
   return utils.get_config.sendMessage(client,message,result)
#data la lingua e la parola chiave da cercare, restituisce il numero massimo di frasi(limite della libreria) della voce trovata
def wikiall(keyword,client,message,lang="it"):
   wikipedia.set_lang(lang)
   if "random" in keyword:
       result = wikirandom(10,client,message,lang)
       return result
   result = wikipedia.summary(keyword,sentences = 10)
   result = result.replace("==","****")
   result += "\n"+create_link(keyword,lang)
   return utils.get_config.sendMessage(client,message,result)
#data la lingua restituisce una frase di una pagina wikipedia casuale
def wikirandom(sents,boole,client,message,lang="it"):
    wikipedia.set_lang(lang)
    wikipedia.set_rate_limiting(rate_limit = True)
    random = wikipedia.random()
    result = wikipedia.summary(random,sentences=sents)
    if boole:
        return result
    else:
        result += "\n"+create_link(random,lang)
        return utils.get_config.sendMessage(client,message,result)
#Simpatica funzione che cerca un comune su Wikipedia e ne restituisce i dati evidenziando numero abitanti e numero pagine visitate per trovarlo.
#Il numero di abitanti viene recuperato direttamente dalla pagina html tramite l'uso della zuppa
@Client.on_message()
def comune(client,message):
    chat = utils.get_config.get_chat(message)
    id_messaggio = utils.get_config.get_id_msg(message)
    count = 0
    client.send_message(chat,"Cerco un comune...","html",reply_to_message_id=id_messaggio)
    wikipedia.set_lang("it")
    while(True):
        count += 1
        client.edit_message_text(chat,id_messaggio+1,"Cerco un comune...\nVoci consultate: " + str(count))
        try:
            random = wikipedia.random()
            result = wikipedia.summary(random,1)
        except:
            continue 
        if (("è un comune" in result or "città" in result or "centro abitato" in result or "è una frazione" in result)):
            page = wikipedia.page(random)
            title = page.title
            page = page.html()
            zuppa = BeautifulSoup(page,"html.parser")
            table = zuppa.find('table',attrs={"class": 'sinottico'})
            text = table.get_text()
            text = text.split("\n")
            for i in range(len(text)):
                if text[i].startswith("Abitanti"):
                    abitanti = text[i]
                    break
            temp = abitanti.split("(")
            abitanti = temp[0]
            abitanti = abitanti.replace("Abitanti","")
            abitanti = abitanti.split("[")
            abitanti = abitanti[0]
            break
    result = "**" + title + "**" + "\n" + result + "\n\n" + "**" + "Abitanti:** " + "**" + abitanti + "**" + "\n\n__Voci consultate:__ " + str(count)
    title = title.replace(" ","_")
    link = "<a href=\"https://it.wikipedia.org/wiki/"+title+"\">Guarda su Wikipedia</a>"
    client.edit_message_text(chat,id_messaggio+1,result + "\n" + link,disable_web_page_preview=True)
    return
