from utils.get_config import sendMessage,get_chat,get_id_msg,sendPhoto
from pyrogram import Client,errors
import requests
import pandas as pd

"""
Restituisce le informazioni relative al comune richiesto
"""
def get_info_comune(comune):
    result = ""
    comune_dt = pd.read_csv("https://raw.githubusercontent.com/opendatasicilia/comuni-italiani/main/dati/main.csv")
    nome = comune
    lat = comune_dt[comune_dt["comune"] == comune]["lat"].unique()[0]
    lon = comune_dt[comune_dt["comune"] == comune]["long"].unique()[0]
    provincia = comune_dt[comune_dt["comune"] == comune]["den_prov"].unique()[0]
    sigla_provincia = comune_dt[comune_dt["comune"] == comune]["sigla"].unique()[0]
    regione = comune_dt[comune_dt["comune"] == comune]["den_reg"].unique()[0]
    cap = comune_dt[comune_dt["comune"] == comune]["cap"].unique()[0]
    website = comune_dt[comune_dt["comune"] == comune]["sito_web"].unique()[0]
    wiki = comune_dt[comune_dt["comune"] == comune]["wikipedia"].unique()[0]
    stemma = comune_dt[comune_dt["comune"] == comune]["stemma"].unique()[0]
    result += "**" + nome + "**\nCoordinate: __" + str(lat) + "," + str(lon) + "__\n" + "Provincia: __" + provincia + " " + sigla_provincia + "__\nRegione: __" + regione + "__\nCAP __: " + str(int(cap)) + "__\n<a href=" + website.replace("http","https") + ">Sito web</a>\n<a href=" + wiki +">Wikipedia</a>\n" + ";" + stemma
    return result


"""
Formatto la stringa nel caso di nessun allerta per renderla più corta.
"""
def format_allerta(allerta):
    if "Assenza di fenomeni significativi prevedibili / NESSUNA ALLERTA" in str(allerta):
        return "__Nessuna allerta__"
    elif "nan" == str(allerta):
        return "__Informazioni non disponibili__"
    else:
        return "__" + str(allerta) + "__"

"""
restituisce previsioni di oggi e domani su eventi estremi nella località richiesta
"""
def get_extreme_forecast(query,client,message):
    bollettino_oggi = pd.read_csv("https://raw.githubusercontent.com/opendatasicilia/DPC-bollettini-criticita-idrogeologica-idraulica/main/data/bollettini/bollettino-oggi-comuni-latest.csv")
    bollettino_domani = pd.read_csv("https://raw.githubusercontent.com/opendatasicilia/DPC-bollettini-criticita-idrogeologica-idraulica/main/data/bollettini/bollettino-domani-comuni-latest.csv")
    if "-z" in query:
        query = query.replace("-z ","").title()
        n = len(bollettino_oggi[bollettino_oggi["zona_codice"]==query])
        return get_extreme_byZone(n,query,client,message)
    query = query.title()
    result = ""
    #recupero informazioni sul comune con funzione dedicata da un altro csv
    comune = get_info_comune(query)
    #recupero l'immagine dello stemma del comune
    url_stemma = comune.split(";")[1]
    result += comune.split(";")[0] + "\n"
    #recupero dati dai 2 csv caricati
    criticita_oggi = format_allerta(bollettino_oggi[bollettino_oggi["comune_nome"] == query]["avviso_criticita"].unique()[0])
    criticita_domani = format_allerta(bollettino_domani[bollettino_domani["comune_nome"] == query]["avviso_criticita"].unique()[0])
    idrogeologico_oggi = format_allerta(bollettino_oggi[bollettino_oggi["comune_nome"] == query]["avviso_idrogeologico"].unique()[0])
    idrogeologico_domani = format_allerta(bollettino_domani[bollettino_domani["comune_nome"] == query]["avviso_idrogeologico"].unique()[0])
    temporali_oggi = format_allerta(bollettino_oggi[bollettino_oggi["comune_nome"] == query]["avviso_temporali"].unique()[0])
    temporali_domani = format_allerta(bollettino_domani[bollettino_domani["comune_nome"] == query]["avviso_temporali"].unique()[0])
    idraulico_oggi = format_allerta(bollettino_oggi[bollettino_oggi["comune_nome"] == query]["avviso_idraulico"].unique()[0])
    idraulico_domani = format_allerta(bollettino_domani[bollettino_domani["comune_nome"] == query]["avviso_idraulico"].unique()[0])
    zona_codice = bollettino_oggi[bollettino_oggi["comune_nome"] == query]["zona_codice"].unique()[0]
    #preparo la stringa finale da inviare come messaggio
    result += "Codice zona: __" + zona_codice + "\n\n"
    result +="**Previsioni di oggi:**\nAvviso di criticità: " + criticita_oggi + "\nAvviso idrogeologico: " + idrogeologico_oggi + "\nAvviso temporali: " + temporali_oggi + "\nAvviso idraulico: " + idraulico_oggi + "\n\n"
    result +="**Previsioni di domani:**\nAvviso di criticità: " + criticita_domani + "\nAvviso idrogeologico: " + idrogeologico_domani + "\nAvviso temporali: " + temporali_domani + "\nAvviso idraulico: " + idraulico_domani 
    return sendPhoto(client,message,url_stemma,result)

"""
Come sopra ma esteso a una zona regionale richiesta 
"""
def get_extreme_byZone(n,query,client,message):
    bollettino_oggi = pd.read_csv("https://raw.githubusercontent.com/opendatasicilia/DPC-bollettini-criticita-idrogeologica-idraulica/main/data/bollettini/bollettino-oggi-zone-latest.csv")
    bollettino_domani = pd.read_csv("https://raw.githubusercontent.com/opendatasicilia/DPC-bollettini-criticita-idrogeologica-idraulica/main/data/bollettini/bollettino-domani-zone-latest.csv")
    criticita_oggi = format_allerta(bollettino_oggi[bollettino_oggi["zona_codice"] == query]["avviso_criticita"].unique()[0])
    criticita_domani = format_allerta(bollettino_domani[bollettino_domani["zona_codice"] == query]["avviso_criticita"].unique()[0])
    idrogeologico_oggi = format_allerta(bollettino_oggi[bollettino_oggi["zona_codice"] == query]["avviso_idrogeologico"].unique()[0])
    idrogeologico_domani = format_allerta(bollettino_domani[bollettino_domani["zona_codice"] == query]["avviso_idrogeologico"].unique()[0])
    temporali_oggi = format_allerta(bollettino_oggi[bollettino_oggi["zona_codice"] == query]["avviso_temporali"].unique()[0])
    temporali_domani = format_allerta(bollettino_domani[bollettino_domani["zona_codice"] == query]["avviso_temporali"].unique()[0])
    idraulico_oggi = format_allerta(bollettino_oggi[bollettino_oggi["zona_codice"] == query]["avviso_idraulico"].unique()[0])
    idraulico_domani = format_allerta(bollettino_domani[bollettino_domani["zona_codice"] == query]["avviso_idraulico"].unique()[0])
    result = "Codice zona: __" + query + "\nIn questa area geografica sono compresi __" + str(n) + "__ comuni.\n\n"
    result +="**Previsioni di oggi:**\nAvviso di criticità: " + criticita_oggi + "\nAvviso idrogeologico: " + idrogeologico_oggi + "\nAvviso temporali: " + temporali_oggi + "\nAvviso idraulico: " + idraulico_oggi + "\n\n"
    result +="**Previsioni di domani:**\nAvviso di criticità: " + criticita_domani + "\nAvviso idrogeologico: " + idrogeologico_domani + "\nAvviso temporali: " + temporali_domani + "\nAvviso idraulico: " + idraulico_domani 
    sendMessage(client,message,result)
    
