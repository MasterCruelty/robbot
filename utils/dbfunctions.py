import sys
sys.path.append(sys.path[0] + "/..")
from utils.dbtables import *
from pyrogram import Client
from utils.get_config import *
import peewee

#Inizio della connessione con il db
db.connect()


####################################################################    
#### FUNZIONI LEGATE ALLE STATISTICHE SUI COMANDI USATI DAGLI UTENTI
####################################################################    
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
    Modifica forzata del numero di volte associato a un comando per un utente
"""
def force_update_stats(client,message,query):
    splitted = query.split(" ")
    userid = int(splitted[0])
    command = splitted[1]
    value = int(splitted[2])
    query = (Stats
             .update({Stats.times : value})
             .where((Stats.id_user == userid) &
                    (Stats.command == command))).execute()
    return sendMessage(client,message,"__Valore aggiornato su " + command + " per " + str(userid) + "__")


"""
    Cancella una riga dalla tabella per l'utente scelto e il comando selezionato
"""
def force_delete_stats(client,message,query):
    splitted = query.split(" ")
    userid = int(splitted[0])
    command = splitted[1]
    query = (Stats
             .delete()
             .where((Stats.id_user == userid) &
                    (Stats.command == command))).execute()
    result = "Comando " + command + " eliminato dalle statistiche di " + str(userid)
    return sendMessage(client,message,result)
             

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


######################################    
#### FUNZIONI LEGATE AL GIOCO /TRIVIAL
######################################    

"""
    @params utente,punteggio,categoria

    Aggiorna il punteggio dell'utente sulla categoria
"""
def update_trivial_score(utente,punteggio,categoria,client,message):
    query = (Trivial
            .update({Trivial.points: Trivial.points + punteggio})
            .where((Trivial.id_user == utente) &
                   (Trivial.category == categoria))).execute()
    if(query == 0):
        score = Trivial(id_user = utente,category = categoria, points = punteggio)
        try:
            score.save()
        except peewee.PeeweeException:
            #Se un utente non registrato vota su un quiz, viene registrato in automatico
            set_user(client,message,utente)
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
    k = 1
    for item in query:
        result += str(k) + ". " + item.user + ": __" + str(item.count) + " punti.__\n"
        k = k + 1
    return sendMessage(client,message,result)

"""
    classifica globale ma solo in una specifica categoria di domande
"""
def global_trivial_leaderboard_category(query,client,message):
    if query == '/globaltscore':
        return global_trivial_leaderboard(client,message)
    query_sql = (User
            .select(User.name.alias('user'),fn.SUM(Trivial.points).alias('count'))
            .join(Trivial, on=(User.id_user == Trivial.id_user))
            .where(Trivial.category == query)
            .order_by(fn.SUM(Trivial.points).desc())
            .group_by(User.id_user))
    result = "__" + query + "__\n"
    k = 1
    for item in query_sql:
        result += str(k) + ". " + item.user + ": __" + str(item.count) + " punti.__\n"
        k = k + 1
    return sendMessage(client,message,result)


"""
    Salva in db i dati del trivial in corso
"""
def save_trivial_data(group,msg,difficulty,categ,question_type):
    trdata = TrivialSavedData(id_chat = group, id_msg = msg, diff = difficulty, category = categ,qtype = question_type)
    trdata.save()
    print("Dati trivial salvati")
    return

"""
    prelevo i dati dei trivial salvati su db
"""
def get_trivial_data():
    query = TrivialSavedData.select()
    print("Dati trivial prelevati")
    return query

"""
    cancella un record dalla tabella dei trivial salvati
"""
def delete_trivial_data(msg):
    query = (TrivialSavedData
             .delete()
             .where(TrivialSavedData.id_msg == msg)).execute()
    print("Dati trivial concluso eliminati")
    return


#############################################################################    
#### FUNZIONI LEGATE ALLA GESTIONE DEI GRUPPI SALVATI CON COMANDI AUTORIZZATI
#############################################################################    

"""
    Restituisce la lista dei gruppi autorizzati a certi comandi
"""
@Client.on_message()
def list_group(client,message):
    result = "Gruppi salvati:\n\n"
    query = Group.select()
    for group in query:
        result += str(group.id_group) + ";" + group.title + ";" + group.command + "\n"
    return sendMessage(client,message,result)


"""
    setto il gruppo come unico autorizzato a un particolare comando
"""
@Client.on_message()
def set_group(client,message,query):
    #splitto sullo spazio poichè l'input è del tipo /setgroup <id gruppo> <comando>
    splitted = query.split(" ")
    json_group = client.get_chat(splitted[0])
    group_id = json_group.id
    title = json_group.title
    command = splitted[1]
    
    #inserisco in db
    group = Group(id_group = group_id,title = title,command = command)
    group.save()
    #verifico sia inserito correttamente
    query = Group.select().where(Group.id_group == group_id)
    for item in query:
        result = "Gruppo " + str(item.id_group) + " registrato con comando " + command
    return sendMessage(client,message,result)

"""
    Cancella il gruppo selezionato dai gruppi autorizzati a determinati comandi
"""
@Client.on_message()
def del_group(client,message,query):
    delete = Group.delete().where(Group.id_group == query).execute()
    result = "Gruppo " + str(query) + " eliminato dai gruppi salvati."
    return sendMessage(client,message,result)

"""
    controllo se il gruppo è autorizzato a eseguire un determinato comando
"""
def check_group_command(match,message):
    query = (Group
            .select()
            .where((Group.id_group == get_chat(message)) &
                   (Group.command == match))).execute()

    #controllo se vi è almeno un record
    i = 0
    for item in query:
        i = i + 1
    if i == 0:
        return True
    else:
        return False


##############################################################    
#### FUNZIONI LEGATE ALLA GESTIONE DEGLI UTENTI SALVATI SUL DB
##############################################################    
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
    update dei dati sul db di un utente specifico
"""
@Client.on_message()
def update_user(client,message,query):
    json_user = client.get_users(query)
    userid = json_user.id
    nome_utente = json_user.first_name
    username_utente = "@" + str(json_user.username)
    query = (User
             .update(name = nome_utente,username = username_utente)
             .where(User.id_user == userid)).execute()
    result = "Dati aggiornati per utente " + str(userid)
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
