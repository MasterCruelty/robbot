import sys
sys.path.append(sys.path[0] + "/..")
from utils.dbtables import *
from pyrogram import Client
from utils.get_config import *

#Inizio della connessione con il db
db.connect()


"""
    @params utente, comando

    dato un id utente e un comando, la funzione aggiorna il conteggio delle volte in cui l'utente ha usato quel comando.
    se il comando è mystat fa subito una return perché lo escludiamo.
"""
def update_stats(utente,comando):
    if(comando == "/mystat"):
        return
    query = (Stats
             .update({Stats.times: Stats.times + 1})
             .where((Stats.id_user == utente) & 
                    (Stats.command == comando))).execute()
    if(query == 0):
        stat = Stats(id_user = utente,command = comando,times = 1)
        stat.save()
    return

"""
    @params client,message,id_utente

    La funzione restituisce tutti i dati sulle statistiche dei comandi usati dall'utente.
"""
def show_stats(utente,client,message):
    id_utente = get_id_user(message)
    result = "Le tue statistiche\n"
    query = (Stats
             .select()
             .join(User, on=(User.id_user == Stats.id_user))
             .where(Stats.id_user == id_utente)
             .order_by(Stats.times.desc()))
    for item in query:
        result += item.command + "__: Usato "  + str(item.times) + " volte.__\n"
    return sendMessage(client,message,result)

"""
    @params utente,punteggio,categoria

    Aggiorna il punteggio dell'utente sulla categoria
"""
def update_trivial_score(utente,punteggio,categoria):
    query = (Trivial
            .update({Trivial.points: Trivial.points + punteggio})
            .where((Trivial.id_user == utente) &
                   (Trivial.category == categoria))).execute()
    if(query == 0):
        score = Trivial(id_user = utente,category = categoria, points = punteggio)
        score.save()
    return

"""
    @params utente,client,message

    Restituisce le proprie statistiche sul gioco Trivial
"""
def personal_trivial_leaderboard(utente,client,message):
    id_utente = get_id_user(message)
    result = "Le tue statistiche su Trivial\n\n"
    query = (Trivial
            .select()
            .join(User, on=(User.id_user == Trivial.id_user))
            .where(Trivial.id_user == id_utente)
            .order_by(Trivial.points.desc()))
    count = 0
    for item in query:
        result += item.category + "__: " + str(item.points) + " punti.__\n"
        count += item.points
    result += "**Punteggio totale: " + str(count) + "**"
    return sendMessage(client,message,result)

"""
    @params client,message
    Classifica globale dei punti su Trivial
"""
def global_trivial_leaderboard(client,message):
    query = (User
            .select(User.name.alias('user'),fn.SUM(Trivial.points).alias('count'))
            .join(Trivial, on=(User.id_user == Trivial.id_user))
            .order_by(fn.SUM(Trivial.points).desc())
            .group_by(User.id_user))

    result = ""
    for item in query:
        result += item.user + ": __" + str(item.count) + " punti.__\n"
    return sendMessage(client,message,result)

"""
questa funzione fa una select dalla tabella User e restituisce gli id di tutti gli utenti registratii dentro una lista di int
"""

def list_id_users():
    result = []
    query = User.select()
    query += Admin.select()
    for user in query:
        result.append(user.id_user)
    return result

"""
questa funzione fa una select dalla tabella User e restituisce i dati di tutti gli utenti in un dato gruppo.
Oppure tutti gli utenti se dato il comando in chat privata
"""
@Client.on_message()
def list_user(client,message):
    result = "Lista utenti salvati:\n\n"
    query = User.select()
    config = get_config_file("config.json")
    id_super_admin = config["id_super_admin"].split(";")
    if(int(get_chat(message)) != int(id_super_admin[0])):
        for user in query:
            try:
                client.get_chat_member(get_chat(message),user.id_user)
                result += str(user.id_user) + ";" + user.name + ";" + user.username + ";Admin: " + str(user.admin) + "\n"
            except:
                continue
    else:
        for user in query:
            result += str(user.id_user) + ";" + user.name + ";" + user.username + ";Admin: " + str(user.admin) + "\n"
    return sendMessage(client,message,result)

"""
questa funzione è simile a list_user ma restituisce solo il numero degli utenti registrati nella tabella User
"""

def all_user(client,message):
    count = 0
    query = User.select()
    for user in query:
        count += 1
    result = "Totale utenti registrati: " + str(count)
    return sendMessage(client,message,result)

"""
questa funzione permette di registrare un nuovo utente nella tabella User
"""
@Client.on_message()
def set_user(client,message,query):
    json_user = client.get_users(query)
    userid = json_user.id
    nome_utente = json_user.first_name
    username_utente = "@" + str(json_user.username)
    user = User(id_user = userid, name = nome_utente, username = username_utente)
    try:
        user.save()
    except:
        return sendMessage(client,message,"Utente già registrato")
    query = User.select().where(User.id_user == userid)
    for user in query:
        result = "Utente " + str(user.id_user) + " salvato!"
    return sendMessage(client,message,result) 

"""
Questa funzione elimina un utente dalla tabella User
"""
@Client.on_message()
def del_user(client,message,query):
    json_user = client.get_users(query)
    userid = json_user.id
    query = User.delete().where(User.id_user == userid).execute()
    result = "Utente " + str(userid) + " eliminato."
    return sendMessage(client,message,result)

"""
Questa funzione controlla se un certo utente Telegram è registrato nella tabella User
"""

def isUser(id_utente):
    if isSuper(id_utente) or isAdmin(id_utente):
        return True
    else:
        check = User.select().where(User.id_user == id_utente)
        for user in check:
            return True
        return False

"""
questa funzione permette di registrare un nuovo admin nella tabella Admin
"""
@Client.on_message()
def set_admin(client,message,query):
    json_user = client.get_users(query)
    userid = json_user.id
    nome_utente = json_user.first_name
    username_utente = "@" + str(json_user.username)
    admin = User(id_user = userid, name = nome_utente, username = username_utente, admin = True)
    try:
        admin.save()
    except:
        admin = User.update({User.admin: True}).where(User.id_user == userid).execute()
        return sendMessage(client,message,"Permessi admin aggiunti a " + str(userid))
    query = User.select().where(User.id_user == userid)
    for admin in query:
        result = "Admin " + str(admin.id_user) + " salvato!"
    return sendMessage(client,message,result)

"""
Questa funzione elimina un admin  dalla tabella Admin
"""
@Client.on_message()
def del_admin(client,message,query):
    json_user = client.get_users(query)
    userid = json_user.id
    query = User.update({User.admin: False}).where(User.id_user == userid).execute()
    result = "Admin " + str(userid) + " revocato."
    return sendMessage(client,message,result) 

"""
Questa funzione controlla se un certo utente Telegram è registrato nella tabella Admin
"""

def isAdmin(id_utente):
    if isSuper(id_utente):
        return True
    else:
        check = User.select().where((User.id_user == id_utente) & 
        (User.admin == True))
        for admin in check:
            return True
        return False

"""
Questa funzione controlla se un certo utente Telegram è SuperAdmin
"""

def isSuper(id_utente):
    check = User.select().where((User.id_user == id_utente) &
            ((User.superadmin == True) & 
            (User.admin == True)))
    for superadmin in check:
        return True
    return False

#chiusura della connessione con il db
db.close()
