import os
import requests
import json
import utils.get_config

"""
    Funzione di supporto che decide quale funzione covid deve essere eseguita
"""
def execute_covid(client,message,query):
    if(query != "/covid"):
        return covidRegions(client,message,query)
    else:
        return covid_daily(client,message)

"""
    Identica a covid_daily ma fornisce i dati della regione richiesta.
"""
def covidRegions(client,message,query):
    url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni-latest.json'
    resp = requests.get(url)
    data = json.loads(resp.text)
    trovata = False
    for item in data:
        if query.title()[0:4] in item["denominazione_regione"]:
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
    if(trovata):
        result = "I nuovi positivi in data **" + giorno +"** nella regione __**" + regione + "**__  sono: **" + nuovi_positivi + "**\nAttualmente vi sono:\n\n __pazienti ricoverati con sintomi:__ **" +ricoverati +"**\n __pazienti in terapia intensiva:__ **" + terapia_intensiva + "**\n __pazienti in isolamento domiciliare:__ **" + isolamento + "**\n __ pazienti deceduti:__ **" + deceduti + "**\n\n" + "__ingressi t.i. :__ **" + ingressi_ti + "**\n__variazione positivi:__ **" + var_positivi + "**"
        return utils.get_config.sendMessage(client,message,result)
    else:
        return utils.get_config.sendMessage(client,message,"__Regione non trovata__")



"""
    funzione che prende ogni giorno il json aggiornato contenente i dati dei contagiati in Italia.
    Direttamente dal repository git di salute.gov.it
"""
def covid_daily(client,message):
    url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale-latest.json'
    resp = requests.get(url)
    data = json.loads(resp.text)
    for item in data:
        nuovi_positivi = str(item["nuovi_positivi"])
        var_positivi = str(item["variazione_totale_positivi"])
        ricoverati = str(item["ricoverati_con_sintomi"])
        terapia_intensiva = str(item["terapia_intensiva"])
        ingressi_ti = str(item["ingressi_terapia_intensiva"])
        isolamento = str(item["isolamento_domiciliare"])
        deceduti = str(item["deceduti"])
        giorno = str(item["data"])[0:10]
    result = "I nuovi positivi in data **" + giorno +"** in **__Italia**__ sono: **" + nuovi_positivi + "**\nAttualmente vi sono:\n\n __pazienti ricoverati con sintomi:__ **" +ricoverati +"**\n __pazienti in terapia intensiva:__ **" + terapia_intensiva + "**\n __pazienti in isolamento domiciliare:__ **" + isolamento + "**\n __ pazienti deceduti:__ **" + deceduti + "**\n\n" + "__ingressi t.i. :__ **" + ingressi_ti + "**\n__variazione positivi:__ **" + var_positivi + "**"
    return utils.get_config.sendMessage(client,message,result)


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
    client,message => parametri necessari per poter usare sendMessage del modulo 'get_config'

    Funzione che restituisce i dati italiani relativi ai vaccini covid19 in termini di dosi consegnate, somministrate e altri dati.
"""
def vaccine(client,message):
    data_total = vaccine_format_json('https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/vaccini-summary-latest.json')
    data_consegne_fornitori = vaccine_format_json('https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/consegne-vaccini-latest.json')
    data_somministrazioni = vaccine_format_json('https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.json')
    total_consegne = 0
    total_somm = 0
    for item in data_total:
        total_consegne += item["dosi_consegnate"]
        total_somm += item["dosi_somministrate"]
    perc = str(round(((total_somm * 100) / total_consegne),2))
    giorno = str(data_total[0]["ultimo_aggiornamento"])[0:10]
    pfizer, moderna, astra = 0,0,0
    for item in data_consegne_fornitori:
        if("Pfizer" in item["fornitore"]):
            pfizer += item["numero_dosi"]
        if("Moderna" in item["fornitore"]):
            moderna += item["numero_dosi"]
        if("AstraZeneca" in item["fornitore"]):
            astra += item["numero_dosi"]
    over80 = 0
    for item in data_somministrazioni:
        over80 += item["categoria_over80"]
    result = "Dati complessivi sui vaccini in __**Italia**__ :\n**__Ultimo aggiornamento: " + giorno + "__**\n\n**Dosi consegnate:** __" + format_values(total_consegne) + "__\n**Dosi somministrate:** __" + format_values(total_somm) + "__\n**Percentuale dosi somministrate:** __" + str(perc) + "%__\n**Over 80 vaccinati:** __" + format_values(over80) +"__\n\nTra le dosi consegnate vi sono:\n**Pfizer-BioNtech:** __" + format_values(pfizer) + "__\n**Moderna:** __" + format_values(moderna) + "__\n**AstraZeneca:** __" + format_values(astra) +"__"
    return utils.get_config.sendMessage(client,message,result)

