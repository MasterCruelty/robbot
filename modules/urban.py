import urbandictionary as ud
from utils.get_config import * 
from pyrogram import Client,filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup,CallbackQuery
from pyrogram.handlers import CallbackQueryHandler

#variabili globali indispensabili per usare i dati della prima funzione sulla seconda
global pages
global k
"""
    Restituisce le definizioni di urban dictionary della parola richiesta
"""
@Client.on_message()
def urban_search(query,client,message):
    global pages
    global k
    result = ""
    definitions = []
    defs = ud.define(query)
    if len(defs) == 0:
        return sendMessage(client,message,"__Error 404: not found__")
    for item in defs:
        result = "**" + item.word + "**"
        result += "\n**Definition:**\n" + item.definition + "\n"
        result += "**Example:** __" + item.example + "__\n\n"
        definitions.append(result)
    
    #I build the keyboard
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("Next",callback_data="NEXT")] ])
    
    #Uso una globale così posso usarla anche dentro press_button
    pages = definitions
    #Aggiungo il callback handler così che Client sappia che al premere del bottone deve richiamare la funzione passata come argomento.
    client.add_handler(CallbackQueryHandler(callback=press_button))
    #Mando il messaggio con la prima pagina
    k = 0
    client.send_message(get_chat(message),pages[k],reply_markup=kb)

"""
    Funzione che viene chiamata quando il bottone costruito alla funzione urban_search viene premuto.
    Utilizza le variabili globali di cui una popolata in urban_search e l'altra viene modificata qui.
"""
@Client.on_callback_query(filters = filters.regex("NEXT"))
def press_button(client,message):
    global k
    if k < len(pages)-1:
        k = k + 1
        kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("Next",callback_data="NEXT")] ])
        message.edit_message_text(pages[k],reply_markup=kb)
    else:
        message.edit_message_text("__Fine__")
