import time
import utils.get_config


"""
    query => tempo nella forma "ns" "nm" "nh" "ngg" dove n è il numero di secondi/minuti/ore/giorni
    funzione di supporto che converte il tempo dalla forma astratta del messaggio in secondi effettivi.
"""
def setTime(client,message,query):
    result = 0
    temp = []
    while("s" in query or "m" in query or "h" in query or "gg" in query):
        try:
            if "gg" in query:
                temp = query.split("gg")
                result += int(temp[0]) * 86400
                query = temp[1]
            if "h" in query:
                temp = query.split("h")
                result += int(temp[0]) * 3600
                query = temp[1]
            if "m" in query:
                temp = query.split("m")
                result += int(temp[0]) * 60
                query = temp[1]
            if "s" in query:
                temp = query.split("s")
                result += int(temp[0])
                query = temp[1]
        except:
            return utils.get_config.sendMessage(client,message,"__formato non valido__")
    if(checktime(result) or result == 0):
        return utils.get_config.sendMessage(client,message,"__Range tempo promemoria non valido__")
    return result


"""
    countdown => tempo in secondi
    Funzione di supporto che controlla il range di tempo richiesto per il promemoria se negativo o troppo alto.
"""
def checktime(countdown):
    if(countdown < 0 or countdown > 86400*7 or countdown == 0):
        return True
    else:
        return False
"""
    client, message => parametri che servono per usare sendMessage da utils.get_config
    query => tempo + messaggio
    Funzione che dato un parametro di tempo e un messaggio da inviare, calcola il countdown nel quale stare fermo in sleep e successivamente invia il messaggio.
"""
def set_reminder(query,client,message):
    split = query.split(";")
    countdown = setTime(client,message,split[0])
    if(countdown is None):
        return
    try:
        msg = split[1]
    except:
        return utils.get_config.sendMessage(client,message,"__formato non valido__")
    utils.get_config.sendMessage(client,message,"Te lo ricorderò!")
    time.sleep(countdown)
    return utils.get_config.sendMessage(client,message,msg)
