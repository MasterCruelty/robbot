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
