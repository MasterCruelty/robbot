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

class Admin(BaseModel):
    id_user = IntegerField(unique = True)
    name = CharField()
    username = CharField()

class SuperAdmin(BaseModel):
    id_user = CharField()
    name = CharField()
    username = CharField()

class Group(BaseModel):
    id_group = IntegerField(unique = True)
    title = CharField()


db.connect()
db.create_tables([User,Admin,SuperAdmin])

#Inizializzo il super admin da file di configurazione
overlord = SuperAdmin(id_user = id_super_admin[0], name = id_super_admin[1], username = id_super_admin[2])
overlord.save()
db.close()
