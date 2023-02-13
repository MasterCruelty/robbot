import sys
sys.path.append(sys.path[0] + "/..")
from utils.get_config import *
import openai

config_file = get_config_file("../config.json")
api_openai = config_file["api_openai"]

"""
Dato l'input, viene generato un testo randomico tramite le api di OpenAI
"""
def openai_completion(query,client,message):
    openai.api_key = api_openai
    stop_seq = ""
    if "stop" in query:
        temp = query.split("/")
        stop_seq = temp[0].replace("stop","")
        query = temp[1]
    resp = openai.Completion.create(
            engine="text-davinci-003",
            prompt=query,
            temperature=0.8,
            max_tokens=1024,
            top_p=1,
            stop = stop_seq,
            frequency_penalty=0.8,
            presence_penalty=0.8)
    result = "**" + query + "** " + resp["choices"][0]["text"]
    return sendMessage(client,message,result)

"""
Dato l'input viene generata un'immagina 512x512 tramite l'algoritmo DALLE offerto da OpenAI
"""
def openai_dalle(query,client,message):
    openai.api_key = api_openai
    resp = openai.Image.create(
            prompt=query,
            n=1,
            size="512x512"
        )
    image_url = resp['data'][0]['url']
    return sendPhoto(client,message,image_url,"__Ecco l'immagine generata__")




