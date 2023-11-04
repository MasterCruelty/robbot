import utils_config
from pyrogram import Client

"""
carica il file di configurazione
"""
def get_config_file(json_file):
    config = utils_config.load_config(json_file)
    return utils_config.serialize_config(config)

"""
funzione d'appoggio per inviare messaggi 
"""
@Client.on_message()
def sendMessage(client,message,result):
    client.send_message(get_chat(message),result,disable_web_page_preview=True,reply_to_message_id=get_id_msg(message))

"""
funzione d'appoggio per inviare immagini
"""
@Client.on_message()
def sendPhoto(client,message,result,caption):
    client.send_photo(get_chat(message),result,caption=caption,reply_to_message_id=get_id_msg(message))

"""
funzione d'appoggio per inviare video
"""
@Client.on_message()
def sendVideo(client,message,result,caption):
    client.send_video(get_chat(message),result,caption=caption,file_name='video.mp4',reply_to_message_id=get_id_msg(message))

"""
funzione d'appoggio per inviare audio
"""
@Client.on_message()
def sendAudio(client,message,result,caption):
    client.send_audio(get_chat(message),result,caption=caption,file_name='audio.mp3',reply_to_message_id=get_id_msg(message))

"""
funzione d'appoggio per inviare gif
"""
@Client.on_message()
def sendGIF(client,message,result,caption):
    client.send_animation(get_chat(message),result,caption=caption,reply_to_message_id=get_id_msg(message))

"""
Restituisce l'id utente
"""
def get_id_user(message):
    try:
        return message.from_user.id
    except AttributeError:
        return "id utente non disponibile"
"""
Restituisce l'id della chat
"""
def get_chat(message):
    try:
        return message.chat.id
    except AttributeError:
        print("Error durante il prelievo dell'id chat")

"""
Restituisce il titolo della chat
"""
def get_chat_name(message):
    try:
        return message.chat.title
    except AttributeError:
        print("Error durante il prelievo del nome della chat")

"""
Restituisce il nome utente
"""
def get_first_name(message):
    try:
        return message.from_user.first_name
    except AttributeError:
        return "Nome utente non disponibile"
"""
Restituisce username dell'utente
"""
def get_username(message):
    try:
        return "@" + str(message.from_user.username)
    except AttributeError:
        return "Non impostato"

"""
Restituisce il campo testo del messaggio
"""
def get_text_message(message):
    if message.text is None:
        return "File multimediale"
    else:
        return message.text
"""
Restituisce l'id del messaggio
"""
def get_id_msg(message):
    return message.id
