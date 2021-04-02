import os
import requests
import json
import utils.get_config

"""
    url => url github da cui recuperare il json

    Funzione di supporto per restituire il json sui contagi da covid19
"""
def covid_format_json(url):
    resp = requests.get(url)
    data = json.loads(resp.text)
    return data

"""
    url => url github da dove prendere il json con i dati.
    
    Funzione di supporto che prende il json e lo formatta per la funzione vaccine.
"""
def vaccine_format_json(url):
    resp = requests.get(url)
    data = json.loads(resp.text)
    return data["data"]

"""
    number => numero da formattare

    Funzione di supporto per formattare i numeri con i separatori per le migliaia.
"""
def format_values(number):
    formated = '{:,}'.format(int(number))
    formated = str(formated).replace(",",".")
    return formated

"""
    repo => json ricavato dalla get al repo github 
    se True il json è vuoto e quindi il problema è esterno al bot, altrimenti è tutto ok.
"""
def check_repo(repo):
    if(repo == []):
        return True
    else:
        return False
"""
    Identica a covid_daily ma fornisce i dati della regione richiesta.
"""
def covid_cases(client,message,query):
    regioni = covid_format_json('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni-latest.json')
    italia  = covid_format_json('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale-latest.json')
    trovata = False
    if(check_repo(regioni) or check_repo(italia)):
        return utils.get_config.sendMessage(client,message,"__Errore repository sorgente__")
    for item in regioni:
        if(query.title()[0:4] in item["denominazione_regione"]):
            regione = item["denominazione_regione"]
            nuovi_positivi = str(item["nuovi_positivi"])
            var_positivi = str(item["variazione_totale_positivi"])
            ricoverati = str(item["ricoverati_con_sintomi"])
            terapia_intensiva = str(item["terapia_intensiva"])
            ingressi_ti = str(item["ingressi_terapia_intensiva"])
            isolamento = str(item["isolamento_domiciliare"])
            deceduti = str(item["deceduti"])
            giorno = str(item["data"])[0:10]
            trovata = True
            break
        elif(query == "/covid"):
            for item in italia:
                regione = "Italia"
                nuovi_positivi = str(item["nuovi_positivi"])
                var_positivi = str(item["variazione_totale_positivi"])
                ricoverati = str(item["ricoverati_con_sintomi"])
                terapia_intensiva = str(item["terapia_intensiva"])
                ingressi_ti = str(item["ingressi_terapia_intensiva"])
                isolamento = str(item["isolamento_domiciliare"])
                deceduti = str(item["deceduti"])
                giorno = str(item["data"])[0:10]
                trovata = True
            break
    if(trovata):
        result = "I nuovi positivi in data **" + giorno +"** in __**" + regione + "**__  sono: **" + format_values(nuovi_positivi) + "**\nAttualmente vi sono:\n\n __pazienti ricoverati con sintomi:__ **" +format_values(ricoverati) +"**\n __pazienti in terapia intensiva:__ **" + format_values(terapia_intensiva) + "**\n __pazienti in isolamento domiciliare:__ **" + format_values(isolamento) + "**\n __pazienti deceduti:__ **" + format_values(deceduti) + "**\n\n" + "__ingressi t.i. :__ **" + format_values(ingressi_ti) + "**\n__variazione positivi:__ **" + format_values(var_positivi) + "**"
        return utils.get_config.sendMessage(client,message,result)
    else:
        return utils.get_config.sendMessage(client,message,"__Regione non trovata__")

"""
    client,message => parametri necessari per poter usare sendMessage del modulo 'get_config'
    query => regione richiesta, di default è l'Italia intera.

    Funzione che restituisce i dati italiani relativi ai vaccini covid19 in termini di dosi consegnate, somministrate e altri dati.
"""
def vaccine(client,message,query):
    data_total = vaccine_format_json('https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/vaccini-summary-latest.json')
    data_consegne_fornitori = vaccine_format_json('https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/consegne-vaccini-latest.json')
    data_somministrazioni = vaccine_format_json('https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.json')
    if(check_repo(data_total)):
        return utils.get_config.sendMessage(client,message,"__Errore repository sorgente__")
    total_consegne = 0
    total_somm = 0
    for item in data_total:
        if(query == "/vaccine"):
            total_consegne += item["dosi_consegnate"]
            total_somm += item["dosi_somministrate"]
            regione = "Italia"
        elif(query.title()[0:4] in item["nome_area"]):
                total_consegne += item["dosi_consegnate"]
                total_somm += item["dosi_somministrate"]
                regione = item["nome_area"]
    if(total_consegne == 0):
        return utils.get_config.sendMessage(client,message,"__Regione non trovata__")
    perc = str(round(((total_somm * 100) / total_consegne),2))
    giorno = str(data_total[0]["ultimo_aggiornamento"])[0:10]
    fornitori = []
    fornitori_somma = [0,0,0,0,0,0,0,0]
    forn_str = ""
    for item in data_consegne_fornitori:
        if(query == "/vaccine"):
            if(item["fornitore"] in fornitori):
                fornitori_somma[fornitori.index(item["fornitore"])] += item["numero_dosi"]
            else:
                fornitori.append(item["fornitore"])
                fornitori_somma[fornitori.index(item["fornitore"])] += item["numero_dosi"]
        elif(query.title()[0:4] in item["nome_area"]):
            if(item["fornitore"] in fornitori):
                fornitori_somma[fornitori.index(item["fornitore"])] += item["numero_dosi"]
            else:
                fornitori.append(item["fornitore"])
                fornitori_somma[fornitori.index(item["fornitore"])] += item["numero_dosi"]
    over80 = 0
    for item in data_somministrazioni:
        if(query =="/vaccine"):
            over80 += item["categoria_over80"]
        else:
            if(query.title()[0:4] in item["nome_area"]):
                over80 += item["categoria_over80"]
    for i in range(len(fornitori)):
        forn_str += "**" + fornitori[i] + ":** __" + format_values(fornitori_somma[i]) + "__\n"
    result = "Dati complessivi sui vaccini in __**" + regione + "**__ :\n**__Ultimo aggiornamento: " + giorno + "__**\n\n**Dosi consegnate:** __" + format_values(total_consegne) + "__\n**Dosi somministrate:** __" + format_values(total_somm) + "__\n**Percentuale dosi somministrate:** __" + str(perc) + "%__\n**Over 80 vaccinati:** __" + format_values(over80) +"__\n\nTra le dosi consegnate vi sono:\n" + forn_str
    return utils.get_config.sendMessage(client,message,result)
