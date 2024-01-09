import sys
sys.path.append(sys.path[0] + "/..")
from utils.get_config import *
from openai import OpenAI
from utils.dbfunctions import isSuper,check_amount

config_file = get_config_file("../config.json")
api_openai = config_file["api_openai"]
client_openai = OpenAI(api_key = api_openai)

"""
Dato l'input, viene generato un testo randomico tramite le api di OpenAI
"""
def openai_completion(query,client,message):
    if not isSuper(get_id_user(message)) or not check_amount(get_id_user(message)):
        return sendMessage(client,message,"__Numero di utilizzi per il tuo profilo: 0\n__")
    stop_seq = ""
    if "stop" in query:
        temp = query.split("/")
        stop_seq = temp[0].replace("stop","")
        query = temp[1]
    resp = client_openai.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": query,
        }
    ],
    model="gpt-3.5-turbo",
    )
    result = "**" + query + "** \n" + resp.choices[0].message.content
    return sendMessage(client,message,result)

"""
Dato l'input viene generata un'immagina 512x512 tramite l'algoritmo DALLE offerto da OpenAI
"""
def openai_dalle(query,client,message):
    try:
        response = client_openai.images.generate(
          model="dall-e-3",
          prompt=query,
          size="1024x1024",
          quality="standard",
          n=1,
        )
    except:
        response = client_openai.images.generate(
          model="dall-e-2",
          prompt=query,
          size="1024x1024",
          quality="standard",
          n=1,
        )

    image_url = response.data[0].url
    return sendPhoto(client,message,image_url,"__Ecco l'immagine generata__")




