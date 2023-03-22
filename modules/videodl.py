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
    yt = pytube.YouTube(url)
    stream = yt.streams.get_highest_resolution()
    #Lo metto in memoria senza salvarlo su disco e lo invio tramite Pyrogram
    video_bytes = io.BytesIO()
    stream.stream_to_buffer(video_bytes)
    video_bytes.seek(0)
    return sendVideo(client,message,video_bytes,"__Ecco il video richiesto__")

