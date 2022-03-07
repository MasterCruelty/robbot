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
    resp = openai.Completion.create(
            engine="text-davinci-001",
            prompt=query,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0)
    result = resp["choices"][0]["text"]
    return sendMessage(client,message,result)
