import sys
sys.path.append(sys.path[0] + "/..")
from utils.dbtables import *
from pyrogram import Client
from utils.get_config import *
import peewee
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import io
import tempfile
matplotlib.use('Agg')

#setto stile matplotlib
plt.style.use('fivethirtyeight')

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
    (Stats
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
    (Stats
     .delete()
     .where((Stats.id_user == userid) &
            (Stats.command == command))).execute()
    result = "Comando " + command + " eliminato dalle statistiche di " + str(userid)
    return sendMessage(client,message,result)
             

"""
    @params client,message,id_utente

    La funzione restituisce tutti i dati sulle statistiche dei comandi usati dall'utente.
"""
def show_stats(query,client,message):
    id_utente = get_id_user(message)
    result = "Le tue statistiche\n"
    query_sql = (Stats
                 .select()
                 .join(User, on=(User.id_user == Stats.id_user))
                 .where(Stats.id_user == id_utente)
                 .order_by(Stats.times.desc()))
    values = []
    labels = []
    no_show_commands = []
    other_value = 0
    total = 0
    #Controllo opzione per ignorare alcuni comandi dalla visualizzazione del piechart
    if "!" in query:
        no_show_commands = str(query.split("!")[1:]).replace("['","").replace("']","").split(",")
    #calcolo il numero totale
    for val in query_sql:
        if val.command not in no_show_commands:
            total += val.times 
    #prelevo i dati dalla query già eseguita pesando per visualizzare un grafico leggibile
    for item in query_sql:
        if (item.times / total) >= 0.005 and (item.command not in no_show_commands):
            labels.append(item.command)
            values.append(item.times)
        elif item.command not in no_show_commands:
            other_value += item.times
        result += item.command + "__: Usato "  + str(item.times) + " volte.__\n"
    #controllo se il valore "altro" è stato modificato e nel caso aggiungo una label dedicata
    if other_value != 0:
        labels.append('Altro')
        values.append(other_value)
    #controllo opzione piechart
    if "-pie" in query:
        #preparo il piechart e salvo l'immagine in RAM
        plt.clf()
        temp = io.BytesIO()
        plt.figure(figsize=(20,15))
        colours = [tuple(np.random.choice(range(256), size=3)/256) + (1,) for n in range(len(labels))]
        plt.pie(values,labels=labels,colors=colours)
        plt.savefig(temp,format='png')
        temp.seek(0)
        image_file = temp
        sendPhoto(client,message,image_file,'__Ecco il grafico a torta prodotto__')
        temp.close()
        image_file.close()
    elif "-bar" in query:
        #non filtro per peso qui
        labels = []
        values = []
        for item in query_sql:
            labels.append(item.command)
            values.append(item.times)
        #preparo il barplot e salvo l'immagine in RAM
        plt.clf()
        temp = io.BytesIO()
        plt.figure(figsize=(20,10))
        plt.subplots_adjust(left=0.2)
        plt.barh(labels,values,color = [tuple(np.random.choice(range(256), size=3)/256) + (1,) for n in range(len(labels))])
        plt.savefig(temp,format='png')
        temp.seek(0)
        image_file = temp
        sendPhoto(client,message,image_file,'__Ecco il grafico a barre prodotto__')
        temp.close()
        image_file.close()
    else:
        sendMessage(client,message,result)

######################################    
#### FUNZIONI LEGATE ALL'USO DI OPENAI
######################################

"""
   @params client, message

   Controllo sul numero di utilizzi rimasti del servizio
   Aggiornamento del numero di utilizzi decrementando di 1
"""
def check_amount(userid):
    query = (OpenAICredit 
            .select()
            .where(OpenAICredit.id_user == userid))
    new_amount = 0
    for item in query:
        if item.amount > 0:
            new_amount = item.amount - 1
            print("Credito ok!")
        else:
            print("Credito non sufficiente")
            return False
    query = (OpenAICredit
            .update({OpenAICredit.amount: new_amount})
            .where(OpenAICredit.id_user == userid)).execute()
    return True

"""
    Restituisce il numero di utilizzi rimasti sul proprio profilo
"""
def show_personal_amount(query,client,message):
    id_user = get_id_user(message)
    if isSuper(id_user):
        return sendMessage(client,message,"__Utilizzi rimasti: ∞__")
    query = (OpenAICredit
            .select()
            .where(OpenAICredit.id_user == id_user))
    amount = 0
    for item in query:
        amount = item.amount
    return sendMessage(client,message,"__Utilizzi rimasti: " + str(amount))

"""
    Restituisce il numero di utilizzi rimasti di ogni utente
"""
def show_all_amounts(client,message,_):
    query = (OpenAICredit
            .select(OpenAICredit.id_user.alias('id'),User.name,OpenAICredit.amount)
            .join(User,on=(User.id_user == OpenAICredit.id_user)))
    result = "Elenco utenti:\n\n"
    for item in query:
        user = str(item.id)
        amount = str(item.amount)
        result += user + ": " + amount + "\n"
    return sendMessage(client,message,result)

"""
    Setta manualmente il nuovo numero di utilizzi in base al credito fornito dall'utente
"""
def set_amount(client,message,query):
    splitted = query.split(" ")
    userid = int(splitted[0])
    new_amount = int(splitted[1])
    query = (OpenAICredit
            .update({OpenAICredit.amount: new_amount})
            .where(OpenAICredit.id_user == userid)).execute()
    if query == 0:
        first_credit = OpenAICredit(id_user = userid,amount = new_amount)
        first_credit.save()
    return sendMessage(client,message,"Credito aggiornato per l'utente " + str(userid))

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

"""
    @params utente,client,message

    Restituisce le proprie statistiche sul gioco Trivial
"""
def personal_trivial_leaderboard(_,client,message):
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
def global_trivial_leaderboard(client,message,category=None):
    if category == '/globaltscore':
        result = ""
        query = (User
                .select(User.id_user.alias('id'),User.name.alias('user'),User.username.alias('nick'),fn.SUM(Trivial.points).alias('count'))
                .join(Trivial, on=(User.id_user == Trivial.id_user))
                .order_by(fn.SUM(Trivial.points).desc())
                .group_by(User.id_user))
    else:
        result = "__" + category + "__\n"
        query = (User
                .select(User.id_user.alias('id'),User.name.alias('user'),User.username.alias('nick'),fn.SUM(Trivial.points).alias('count'))
                .join(Trivial, on=(User.id_user == Trivial.id_user))
                .where(Trivial.category == category)
                .order_by(fn.SUM(Trivial.points).desc())
                .group_by(User.id_user))
    k = 1
    for item in query:
        if item.id == message.from_user.id:
            result += "<code> >>" + str(k) + ". " + item.user + ": " + str(item.count) + " punti.<< </code>\n"
            k = k + 1
            continue
        if len(item.nick) > 15 or item.nick == "@None":
            result += str(k) + ". " + item.user + ": __" + str(item.count) + " punti.__\n"
        else:
            result += str(k) + ". " + item.nick.replace("@","") + ": __" + str(item.count) + " punti.__\n"
        k = k + 1
    return sendMessage(client,message,result)

"""
    classifica globale ma solo in una specifica categoria di domande
"""
def global_trivial_leaderboard_category(query,client,message):
    return global_trivial_leaderboard(client,message,query)


"""
    Salva in db i dati del trivial in corso
"""
def save_trivial_data(group,msg,difficulty,categ,question_type):
    trdata = TrivialSavedData(id_chat = group, id_msg = msg, diff = difficulty, category = categ,qtype = question_type)
    trdata.save()
    print("Dati trivial salvati")

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
    (TrivialSavedData
     .delete()
     .where(TrivialSavedData.id_msg == msg)).execute()
    print("Dati trivial concluso eliminati")


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
    Group.delete().where(Group.id_group == query).execute()
    result = "Gruppo " + str(query) + " eliminato dai gruppi salvati."
    return sendMessage(client,message,result)

"""
    Aggiorna il nome di un gruppo sul db
"""
@Client.on_message()
def update_group(client,message,query):
    json_group = client.get_chat(query)
    (Group
     .update({Group.title: json_group.title})
     .where(Group.id_group == json_group.id)).execute()
    result = "Gruppo " + str(json_group.id ) + " aggiornato con successo!"
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
    for _ in query:
        i = i + 1
    if i == 0:
        return True
    else:
        return False

##############################################################    
#### FUNZIONI LEGATE ALLA GESTIONE DELLE FERMATE ATM SALVATE
##############################################################    
from modules.atm_feature import get_json_atm,handle_except

"""
    Salva sul db una fermata atm preferita dando solo il codice fermata.
    Sulla tabella viene salvato il codice fermata indicato e una descrizione.
    La descrizione contiene i numeri di linea che passano e le loro direzioni.
"""
def save_stop(query,client,message):
    resp = get_json_atm(query)
    data_json = handle_except(resp)
    if str(data_json).startswith("404") or "riprova tra poco" in str(data_json):
        return sendMessage(client,message,"__Non è stato possibile salvare la fermata.__")
    descrizione = data_json["Description"]
    Lines = data_json["Lines"]
    line_code, line_description = ([] for i in range(2))
    for item in Lines:
        Line = item["Line"]
        line_code.append(Line["LineCode"])
        line_description.append(Line["LineDescription"])
    stop_info = "**" + descrizione + "**" + "\n"
    for i in range(len(line_code)):
        stop_info += "__Linea: " + line_code[i] + "\nDirezione: " + line_description[i] + "__\n"
    stop_info += "\n"

    #query sql insert  
    insert_sql = AtmFavStops(id_user = get_id_user(message), favstop_code= query, favstop_lines_info = stop_info)  
    try:
        insert_sql.save()
    except:
        return sendMessage(client,message,"__Questa fermata è già salvata tra le tue preferite.__")
    return sendMessage(client,message,"__La fermata con codice __"+str(query)+"__ è stata salvata.") 

"""
    Restituisce le proprie fermate preferite sotto forma di messaggio.
    Così da poter essere consultate velocemente e usare quella che serve.
"""
def get_stop(query,client,message):
    id_utente = get_id_user(message)
    result = "Le tue fermate preferite:\n"
    query_sql = (AtmFavStops
                 .select()
                 .join(User, on=(User.id_user == AtmFavStops.id_user))
                 .where(AtmFavStops.id_user == id_utente))
    #check if there's at least a record
    i = 0
    for _ in query_sql:
        i = i + 1
    if i == 0:
        return sendMessage(client,message,"__Nessuna fermata salvata.__")
    #building result string
    for item in query_sql:
        result += "\n__CODICE FERMATA: " + item.favstop_code + "__\n" + item.favstop_lines_info
        result += "Puoi Digitare <code>/atm " + item.favstop_code + "</code>\n\n"
    return sendMessage(client,message,result)

"""
    Elimina una fermata atm tra quelle salvate dando il codice fermata
"""
def delete_stop(query,client,message):
    try:
        AtmFavStops.delete().where(AtmFavStops.favstop_code == query).execute()
    except:
        return sendMessage(client,message,"__Non esiste nessuna fermata salvata con questo codice.__")
    return sendMessage(client,message,"__Fermata con codice " + query + " eliminata.")



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
    (User
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
