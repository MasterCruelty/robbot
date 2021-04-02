import time
import utils.get_config

"""
    query => tempo nella forma "ns" "nm" "nh" "ngg" dove n è il numero di secondi/minuti/ore/giorni
    funzione di supporto che converte il tempo dalla forma astratta del messaggio in secondi effettivi.
"""
def setTime(query):
    if "s" in query:
        return int(query.replace("s",""))
    if "m" in query:
        query = query.replace("m","")
        query = int(query) * 60
        return query
    if "h" in query:
        query = query.replace("h","")
        query = int(query) * 3600
        return query
    if "gg" in query:
        query = query.replace("gg","")
        query = int(query) * 86400
        return query
    else:
        return utils.get_config.sendMessage(client,message,"__formato non valido__")

"""
    countdown => tempo in secondi
    Funzione di supporto che controlla il range di tempo richiesto per il promemoria se negativo o troppo alto.
"""
def checktime(countdown):
    if(countdown < 0 or countdown > 86400*7):
        return True
    else:
        return False
"""
    client, message => parametri che servono per usare sendMessage da utils.get_config
    query => tempo + messaggio
    Funzione che dato un parametro di tempo e un messaggio da inviare, calcola il countdown nel quale stare fermo in sleep e successivamente invia il messaggio.
"""
def set_reminder(client,message,query):
    split = query.split("/")
    countdown = setTime(split[0])
    if(checktime(countdown)):
        return utils.get_config.sendMessage(client,message,"__Range tempo promemoria non valido__")
    msg = split[1]
    utils.get_config.sendMessage(client,message,"Te lo ricorderò!")
    time.sleep(countdown)
    return utils.get_config.sendMessage(client,message,msg)
