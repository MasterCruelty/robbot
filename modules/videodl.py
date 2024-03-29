from utils.get_config import sendMessage,sendVideo
from pyrogram import Client,errors
import pytube
import io

not_valid_url = "__url non valido per il download da Youtube__"
download_error = "__Errore durante il download del video richiesto.\nRiprova, se il problema persiste è legato a pytube, quindi usare un altro strumento per il download.__"

"""
    Restituisce il video scaricato da Youtube inviato come media
"""
def youtube_dl(query,client,message):
    url = query
    if not url.startswith("https://www.youtube.com"):
        return sendMessage(client,message,not_valid_url)
    #Scarico il video con pytube
    try:
        yt = pytube.YouTube(url)
        sendMessage(client,message,"__Download in progress...__")
        stream = yt.streams.get_highest_resolution()
        #Lo metto in memoria senza salvarlo su disco e lo invio tramite Pyrogram
        video_bytes = io.BytesIO()
        stream.stream_to_buffer(video_bytes)
    except (KeyError,pytube.exceptions.AgeRestrictedError):
        return sendMessage(client,message,download_error)
    video_bytes.seek(0)
    sendMessage(client,message,"__Upload in progress...__")
    sendVideo(client,message,video_bytes,"__Ecco il video richiesto__")
    #clean the BytesIO file object
    video_bytes.truncate(0)
    video_bytes.seek(0)
    video_bytes.close()

