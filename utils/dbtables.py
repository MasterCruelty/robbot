from peewee import *
import sys
sys.path.append(sys.path[0] + "/..")
from utils.get_config import get_config_file

config = get_config_file("config.json")
id_super_admin = config["id_super_admin"].split(";")
path_db = config["path_db"]

global db
db = SqliteDatabase(path_db)

class BaseModel(Model):
    class Meta:
        database = db

"""
    id_user: id utente
    name: nome utente
    username: username telegram utente
    admin: bool(1 è admin, 0 non lo è)
    superadmin: bool(1 è superadmin, 0 non lo è)
""" 
class User(BaseModel):
    id_user = IntegerField(unique = True)
    name = CharField()
    username = CharField()
    admin = BooleanField(default=False)
    superadmin = BooleanField(default=False)


"""
    command: comando lanciato
    times: numero di volte che è stato lanciato
"""
class Stats(BaseModel):
    id_user = ForeignKeyField(User)
    command = CharField()
    times = IntegerField(default = 0)

"""
    favstop_code: codice fermata
    favstop_lines_info: Nome della fermata
"""
class AtmFavStops(BaseModel):
    id_user = ForeignKeyField(User)
    favstop_code = CharField(unique=True)
    favstop_lines_info = CharField()

"""
    category: categoria di domanda
    points: numero di punti acquisiti
"""
class Trivial(BaseModel):
    id_user = ForeignKeyField(User)
    category = CharField()
    points = IntegerField(default = 0)

"""
    Tabella gruppi per autorizzare un comando solo all'interno di alcuni gruppi
    Campi:
    id gruppo
    nome gruppo
    nome comando
"""
class Group(BaseModel):
    id_group = IntegerField(unique = True)
    title = CharField()
    command = CharField()

"""
    Tabella ausiliaria per salvare i dati del trivial mentre è in corso
    Così da poter avere più trivial contemporaneamente in gioco.
"""
class TrivialSavedData(BaseModel):
    id_chat = IntegerField(default = 0)
    id_msg = IntegerField(unique = True)
    diff = CharField()
    category = CharField()
    qtype = CharField()

"""
    Tabella che definisce lo stato di credito di un utente per i comandi di OpenAI.
    L'attributo amount definisce quanto utilizzo ha ancora del servizio.
"""
class OpenAICredit(BaseModel):
    id_user = ForeignKeyField(User)
    amount  = IntegerField(default = 0)


db.connect()
db.create_tables([User,Stats,Trivial,Group,TrivialSavedData,OpenAICredit])

#Inizializzo il super admin da file di configurazione
overlord = User(id_user = id_super_admin[0], name = id_super_admin[1], username = id_super_admin[2], admin = True, superadmin = True)
try:
    overlord.save()
except:
    db.close()
db.close()
