import os
import requests
import json
import utils.get_config


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
    result = "I nuovi positivi in data " + giorno +" sono: " + nuovi_positivi + "\nAttualmente vi sono:\n" + ricoverati + " pazienti ricoverati con sintomi\n" + terapia_intensiva + " pazienti in terapia intensiva\n" + isolamento + " pazienti in isolamento domiciliare\n" + deceduti + " pazienti deceduti" +"\n\n" + "ingressi t.i. : " + ingressi_ti + "\nvariazione positivi: " + var_positivi
    return utils.get_config.sendMessage(client,message,result)
