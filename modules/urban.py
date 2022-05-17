import urbandictionary as ud
from utils.get_config import sendMessage 


"""
    Restituisce le definizioni di urban dictionary della parola richiesta
"""
def urban_search(query,client,message):
    result = ""
    defs = ud.define(query)
    if len(defs) == 0:
        return sendMessage(client,message,"__Error 404: not found__")
    for item in defs:
        result += "**" + item.word + "**"
        result += "\n" + item.definition + "\n"
        result += "__" + item.example + "__"
    return sendMessage(client,message,result)
