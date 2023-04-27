from utils.get_config import sendMessage,sendVideo
from pyrogram import Client,errors
import pytube
import io


"""
    Restituisce il video scaricato da Youtube inviato come media
"""
def youtube_dl(query,client,message):
    url = query
    if not url.startswith("https://www.youtube.com"):
        return sendMessage(client,message,"__url non valido per il download da Youtube__")
    #Scarico il video con pytube
    try:
        yt = pytube.YouTube(url)
        stream = yt.streams.get_highest_resolution()
        #Lo metto in memoria senza salvarlo su disco e lo invio tramite Pyrogram
        video_bytes = io.BytesIO()
        stream.stream_to_buffer(video_bytes)
    except KeyError:
        return sendMessage(client,message,"__Errore durante il download del video richiesto.\nRiprova, se il problema persiste è legato a pytube, quindi usare un altro strumento.__")
    video_bytes.seek(0)
    sendVideo(client,message,video_bytes,"__Ecco il video richiesto__")
    #clean the BytesIO file object
    video_bytes.truncate(0)
    video_bytes.seek(0)
    video_bytes.close()

