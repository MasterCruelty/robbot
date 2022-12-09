import requests
import json
import utils.get_config as ugc
import pandas as pd

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
    try:
        resp = requests.get(url)
        data = json.loads(resp.text)
    except:
        data = []
        return data
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
    client,message => parametri necessari per poter usare sendMessage del modulo 'get_config'
    query => il tipo di richiesta che farà decidere quale funzione vaccine eseguire.

    Funzione che controlla il parametro query e in funzione di quello decide quale delle funzioni vaccine sarà eseguita.

"""
def check_vaccine_function(query,client,message):
    split_query = query.split(" ")
    if split_query[0].lower() == "punti":
        return vaccinepoints(client,message,split_query)
    else:
        return vaccine(query,client,message)


"""
    client,message => parametri necessari per poter usare sendMessage del modulo 'get_config'
    query => regione richiesta, di default è l'Italia intera.

    Restituisce i dati principali sui contagi da covid19.
"""
def covid_cases(query,client,message):
    regioni = covid_format_json('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni-latest.json')
    italia  = covid_format_json('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale-latest.json')
    trovata = False
    if(check_repo(regioni) or check_repo(italia)):
        return ugc.sendMessage(client,message,"__Errore repository sorgente__")
    for item in regioni:
        if(query.title()[0:5] in item["denominazione_regione"]):
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
        return ugc.sendMessage(client,message,result)
    else:
        return ugc.sendMessage(client,message,"__Regione non trovata__")

"""
    client,message => parametri necessari per poter usare sendMessage del modulo 'get_config'
    split_query => array composto da punti in posizione [0] e la provincia richiesta in posizione [1]

    Funzione che restituisce la lista di punti di somministrazione vaccini nella provincia richiesta mostrandone anche il comune relativo.
"""
def vaccinepoints(client,message,split_query):
    if(len(split_query) == 1):
        return ugc.sendMessage(client,message,"__Errore formato.\n/helprob vaccine per più dettagli sul comando.__")
    data_points = vaccine_format_json('https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/punti-somministrazione-latest.json')
    if(check_repo(data_points)):
        return ugc.sendMessage(client,message,"__Errore repository sorgente__")
    result = "__**Punti di somministrazione trovati nella provincia di " + split_query[1].title() + "__**\n"
    str_points = ""
    provincia = split_query[1]
    for item in data_points:
        if(provincia[0:6].title() in item["provincia"].title()):
            str_points += "**Punto:**  __" + str(item["presidio_ospedaliero"]).title() + "__ **(" + str(item["comune"]).title() + ")**\n"
    if(str_points == ""):
        result = "__**Nessun punto di somministrazione trovato**__"
    else:
        result += str_points
    return ugc.sendMessage(client,message,result)

"""
    client,message => parametri necessari per poter usare sendMessage del modulo 'get_config'
    query => regione richiesta, di default è l'Italia intera.

    Funzione che restituisce i dati italiani relativi ai vaccini covid19 in termini di dosi consegnate, somministrate e altri dati.
"""
def vaccine(query,client,message):
    data_total = pd.read_csv('https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/vaccini-summary-latest.csv')
    data_consegne_fornitori = pd.read_csv('https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/consegne-vaccini-latest.csv')
    data_somministrazioni = pd.read_csv('https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv')
    total_consegne = 0
    total_somm = 0
    if(query == "/vaccine"):
        total_consegne = sum(data_total["dosi_consegnate"])
        total_somm = sum(data_total["dosi_somministrate"])
        regione = "Italia"
    else:
        for i in data_total['reg'].unique():
            if query.title() in i:
                regione = i
        total_consegne = sum(data_total[data_total['reg'] == regione]["dosi_consegnate"])
        total_somm = sum(data_total[data_total['reg'] == regione]["dosi_somministrate"])
    if(total_consegne == 0):
        return ugc.sendMessage(client,message,"__Errore formato.\n/helprob vaccine per più dettagli sul comando.__")
    perc = str(round(((total_somm * 100) / total_consegne),2))
    giorno = str(data_total["ultimo_aggiornamento"].unique()[0])
    fornitori = data_consegne_fornitori['forn'].unique()
    fornitori_somma = []
    forn_str = ""
    prima_dose = seconda_dose = dose_booster = 0
    if(query == "/vaccine"):
        for i in fornitori:
            fornitori_somma.append(sum(data_consegne_fornitori[data_consegne_fornitori['forn'] == i]['numero_dosi']))
        prima_dose = sum(data_somministrazioni["d1"])
        seconda_dose = sum(data_somministrazioni["d2"])
        dose_booster = sum(data_somministrazioni["db1"]) + sum(data_somministrazioni["db2"])
    else:
        for i in fornitori:
            fornitori_somma.append(sum(data_consegne_fornitori[(data_consegne_fornitori['forn'] == i) & (data_consegne_fornitori['reg'] == regione)]['numero_dosi']))
        prima_dose = sum(data_somministrazioni[data_somministrazioni['reg'] == regione]["d1"])
        seconda_dose = sum(data_somministrazioni[data_somministrazioni['reg'] == regione]["d2"])
        dose_booster = sum(data_somministrazioni[data_somministrazioni['reg'] == regione]["db1"]) + sum(data_somministrazioni[data_somministrazioni['reg'] == regione]["db2"])
    for i in range(len(fornitori)):
        forn_str += "**" + fornitori[i] + ":** __" + format_values(fornitori_somma[i]) + "__\n"
    result = "Dati complessivi sui vaccini in __**" + regione + "**__ :\n**__Ultimo aggiornamento: " + giorno + "__**\n\n**Dosi consegnate:** __" + format_values(total_consegne) + "__\n**Dosi somministrate:** __" + format_values(total_somm) + "__\n\n**Percentuale dosi somministrate:** __" + str(perc) + "__\n**Totale prime dosi:** __" + format_values(prima_dose) + "__\n**Totale seconde dosi:** __" + format_values(seconda_dose) + "__\n**Totale dosi booster:** __" + format_values(dose_booster) + "__\n\nTra le dosi consegnate vi sono:\n" + forn_str
    return ugc.sendMessage(client,message,result)
