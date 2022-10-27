import urbandictionary as ud
from utils.get_config import * 
from pyrogram import Client
from pyrogram.types import (InlineKeyboardButton,InlineKeyboardMarkup,CallbackQuery)


"""
    Restituisce le definizioni di urban dictionary della parola richiesta
"""
@Client.on_message()
def urban_search(query,client,message):
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
    
    i = 0
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("Next",callback_data="Prossima deifinizione")] ])
    client.send_message(get_chat(message),definitions[i],reply_markup=kb)
    while i < len(definitions):
        i = i + 1
        client.edit_message_text(get_chat(message),id_msg+1,definitions[i],reply_markup=kb)
    #press_button(client,message,kb,definitions,message.id)
    #CallbackQuery.edit_message_text(get_chat(message),message.id+1,definitions[i+1],reply_markup=kb)


@Client.on_callback_query()
def press_button(client,message,kb,definitions,id_msg):
    i = 1
    client.edit_message_text(get_chat(message),id_msg+1,definitions[i],reply_markup=kb)
    i = i + 1
