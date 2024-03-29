import wikipedia
import wikipediaapi
from pyrogram import Client
import utils.get_config as ugc
import utils.controller as uct
from bs4 import BeautifulSoup

wiki_link_starttext = "<a href="
wiki_link_endtext = ">Guarda su Wikipedia</a>"

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
    wikipedia.set_lang(lang)
    page = wikipedia.page(keyword)
    link = wiki_link_starttext + page.url + wiki_link_endtext
    return link

#come sopra ma compatibile con la seconda libreria utilizzata "wikipediaapi"
def create_link_wikiapi(page):
    url = page.fullurl
    link = wiki_link_starttext + url + wiki_link_endtext
    return link
    

#Questa funzione esegue il comando wiki richiesto dall'app principale fetchato tramite la funzione in system.py
@Client.on_message()
def execute_wiki(query,client,message):
    if "/comune" in query:
        try:
            return comune(client,message)
        except:
            client.edit_message_text(ugc.get_chat(message),message.id+1,"Operazione fallita")
            return
    lingua = get_lang(query)
    if (lingua not in wikipedia.languages()) or lingua == "all":
        return exec_wiki_ita(query,client,message)
    if "-s" in query:
        return wikibysection(keyword,client,message,lingua)
    word = get_keyword(query)
    if " all " in query:
        return wikiall(word,client,message,lingua)
    if "-r" in query:
        return wikirandom(1,False,client,message,lingua)
    else:
        return wiki(word,client,message,lingua)


#Esegue le funzioni wiki ma con lingua italiana come default
def exec_wiki_ita(query,client,message):
    if "all " in query:
        query = uct.parser(query)
        return wikiall(query,client,message)
    if "-r" in query:
        return wikirandom(1,False,client,message)
    if "-s" in query:
        query = uct.parser(query)
        return wikibysection(query,client,message)
    else:
        return wiki(query,client,message)



#data la lingua e la parola chiave da cercare, restituisce una frase della voce trovata
def wiki(keyword,client,message,lang="it"):
   wiki = wikipediaapi.Wikipedia('Robbot (example@ex.com)',lang,extract_format=wikipediaapi.ExtractFormat.WIKI) 
   page = wiki.page(keyword)
   if not page.exists():
       return ugc.sendMessage(client,message,"__Page not found.__")
   result = "**" + page.title.title() +"**\n" 
   result += page.summary[0:300] + "\n" + create_link_wikiapi(page)
   result += "\n\n**Sezioni:**\n<code>"
   for item in page.sections:
       result += item.title + "\n"
   result += "</code>"
   return ugc.sendMessage(client,message,result)

#Restituisce una sezione specifica della pagina wikipedia ricercata
def wikibysection(keyword,client,message,lang="it"):
   page_title, section_title = keyword.split("/")
   page_title = page_title.strip()
   section_title = section_title.strip()
   wiki = wikipediaapi.Wikipedia('Robbot (example@ex.com)',lang,extract_format=wikipediaapi.ExtractFormat.WIKI) 
   page = wiki.page(page_title)
   try:
       section = page.section_by_title(section_title).text
   except AttributeError:
        return ugc.sendMessage(client,message,"__Page not found.__")
   if section != '':
       result = "**" + page_title + "\n" + section_title + "**\n" + section 
   else:
       result = "**" + page_title + "**\n"  + str(page.section_by_title(section_title)).replace("Section:","**").replace("Subsections","**").replace("(1):","**").replace("(2):","**").replace("(0):","")
   return ugc.sendMessage(client,message,result)


#data la lingua e la parola chiave da cercare, restituisce i primi paragrafi della voce trovata
def wikiall(keyword,client,message,lang="it"):
   wiki = wikipediaapi.Wikipedia('Robbot (example@ex.com)',lang,extract_format=wikipediaapi.ExtractFormat.WIKI) 
   page = wiki.page(keyword)
   if "-r" in keyword:
       result = wikirandom(10,client,message,lang)
       return result
   result = "**" + page.title.title() + "**\n"
   result += page.text
   try:
       result += "\n"+create_link_wikiapi(page)
   except KeyError:
        result = "__Pagina non trovata__"
   return ugc.sendMessage(client,message,result)



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
        return ugc.sendMessage(client,message,result)



#Simpatica funzione che cerca un comune su Wikipedia e ne restituisce i dati evidenziando numero abitanti e numero pagine visitate per trovarlo.
#Il numero di abitanti viene recuperato direttamente dalla pagina html tramite l'uso della zuppa
@Client.on_message()
def comune(client,message):
    chat = ugc.get_chat(message)
    id_messaggio = ugc.get_id_msg(message)
    count = 0
    client.send_message(chat,"Cerco un comune...",reply_to_message_id=id_messaggio)
    wikipedia.set_lang("it")
    while(True):
        count += 1
        #Stampo solo per numeri pari dimezzando il numero di modifiche al messaggio.
        #Meno carico sulle richieste api di Telegram.
        if count % 2 == 0:
            client.edit_message_text(chat,id_messaggio+1,"Cerco un comune...\nVoci consultate: " + str(count))
        try:
            random = wikipedia.random()
            result = wikipedia.summary(random,1)
        except:
            continue 
        if (("è un comune" in result or "è una curazia" in result or "città" in result or "centro abitato" in result or "è una frazione" in result)):
            page = wikipedia.page(random)
            title = page.title
            page_source = page.html()
            zuppa = BeautifulSoup(page_source,"html.parser")
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
    link = wiki_link_starttext + page.url + wiki_link_endtext
    client.edit_message_text(chat,id_messaggio+1,result + "\n" + link,disable_web_page_preview=True)
    return
