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
    category: categoria di domanda
    points: numero di punti acquisiti
"""
class Trivial(BaseModel):
    id_user = ForeignKeyField(User)
    category = CharField()
    points = IntegerField(default = 0)

class Group(BaseModel):
    id_group = IntegerField(unique = True)
    title = CharField()
    command = CharField()

"""
    valore booleano necessario per non avere due quiz attivi in contemporanea
"""
class waitTrivial(BaseModel):
    value = BooleanField()


db.connect()
db.create_tables([User,Stats,Trivial,waitTrivial])

#Inizializzo il wait trivial a False
wait_trivial = waitTrivial(value = False)
wait_trivial.save()

#Inizializzo il super admin da file di configurazione
overlord = User(id_user = id_super_admin[0], name = id_super_admin[1], username = id_super_admin[2], admin = True, superadmin = True)
try:
    overlord.save()
except:
    db.close()
db.close()
