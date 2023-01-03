from utils.get_config import sendMessage,get_chat,get_id_msg,get_id_user 
from utils.dbfunctions import personal_trivial_leaderboard,global_trivial_leaderboard_category,update_trivial_score,get_trivial_data,save_trivial_data,delete_trivial_data
from pyrogram import Client,errors
from pyrogram.enums import PollType
from pyrogram.handlers import PollHandler,RawUpdateHandler
from pyrogram.raw.types import UpdateMessagePollVote
import requests
import json
import random
import time
from bs4 import BeautifulSoup


categorie = {"General Knowledge"                    :9,
             "Entertainment: Books"                 :10,
             "Entertainment: Film"                  :11,
             "Entertainment: Music"                 :12,
             "Entertainment: Musical & Theatres"    :13,
             "Entertainment: Television"            :14,
             "Entertainment: Video Games"           :15,
             "Entertainment: Board Games"           :16,
             "Science & Nature"                     :17,
             "Science: Computers"                   :18,
             "Science: Mathematics"                 :19,
             "Mythology"                            :20,
             "Sports"                               :21,
             "Geography"                            :22,
             "History"                              :23,
             "Politics"                             :24,
             "Art"                                  :25,
             "Celebrities"                          :26,
             "Animals"                              :27,
             "Vehicles"                             :28,
             "Entertainment: Comics"                :29,
             "Science: Gadgets"                     :30,
             "Entertainment: Japanese Anime & Manga":31,
             "Entertainment: Cartoon & Animations"  :32}


tipo_domanda = {"tf"       :"boolean",
                "multi"    :"multiple"}

response_code = {0:"Ok",
                 1:"No Results",
                 2:"Invalid Parameter",
                 3:"Token not found",
                 4:"Token Empty"}


global token

"""
    Chiamata per la creazione di un token che garantisce l'unicità delle domande fetchate da opentb.com
    Il token ha una vita di 6 ore se inattivo ininterrottamente.
    Una volta esaurito, va resettato e generato di nuovo.
"""
def create_token():
    global token
    url = "https://opentdb.com/api_token.php?command=request"
    resp = requests.get(url)
    data = json.loads(resp.text)
    if data["response_code"] == 0:
        token = data["token"]
    else:
        return response_code[data["response_code"]]
    return token

"""
    Chiamata per il reset del token nel caso in cui sia stato esaurito completamente.
"""
def reset_token():
    global token
    url = "https://opentb.com/api_token.php?command=reset&token=" + token
    resp = requests.get(url)
    data = json.loads(resp.text)
    if data["response_code"] == 0:
        token = data["token"]
    else:
        return response_code[data["response_code"]]
    return token



"""
    Controlla se il token è in buono stato e quindi se non lo è lo resetta o lo crea se non esistente.
"""
def check_token():
    #check token existence
    try:
        if token == None:
            token = create_token()
    except NameError:
        token = create_token()
    #check token is good
    if token == "Token Empty":
        token = reset_token()
    elif len(token) < 17:
        return sendMessage(client,message,token)
    return token


"""
    funzione ausiliaria per settare la difficoltà randomicamente
"""
def set_difficulty():
    difficulty_list = ["easy","medium","hard"]
    random.shuffle(difficulty_list)
    return difficulty_list[0]


"""
    Conversione codifica HTML in testo
"""
def html2text(strings):
    result = []
    for i in range(len(strings)):
        zuppa = BeautifulSoup(strings[i],features="lxml")
        result.append(zuppa.get_text())
    return result

"""
    Come sopra ma per le stringhe singole e non liste
"""
def html2text_str(string):
    zuppa = BeautifulSoup(string,features="lxml")
    result = zuppa.get_text()
    return result

"""
    randomizza se scegliere vero/falso o risposta multipla
"""
def get_question_type():
    #create question type in random mode 
    n = random.randint(0,100)
    question_list = ["tf","multi"]
    if n >= 65:
        question_type = question_list[0]
    else:
        question_type = question_list[1]
    return question_type

"""
    Restituisce una domanda quiz tramite le api di opentdb.com
    Definizione di alcune variabili globali per tenere dei valori in memoria tra una funzione e la callback
"""
@Client.on_message()
def send_question(query,client,message):
    #check token
    global token
    token = check_token()

    #build parameter for request
    if query == "/trivial":
        #Build random options for the request
        category_number = random.randint(9,32)
        question_type = get_question_type() 
        #setting difficulty
        difficulty = set_difficulty()
    else:
        splitted = query.split(" ")
        try:
            category = splitted[0].title()
            for item in categorie:
                if category in item:
                    category_number = categorie[item]
                    break
            question_type = get_question_type()
            difficulty = set_difficulty()
        except IndexError:
            return sendMessage(client,message,"__Errore formato trivial.__")

    #build api url
    api_url = "https://opentdb.com/api.php?amount=1&category=" + str(category_number) + "&difficulty=" + difficulty + "&type=" + tipo_domanda[question_type] + "&token=" + token
    resp = requests.get(api_url)
    data = json.loads(resp.text)
    incorrect = []
    question = ""
    correct = ""
    for item in data["results"]:
        category = item["category"]
        difficulty = item["difficulty"]
        question = item["question"]
        correct = item["correct_answer"]
        incorrect = item["incorrect_answers"]
        incorrect.append(correct)
    random.shuffle(incorrect)
    #prepare question and send
    question  = html2text_str(question)
    correct = html2text_str(correct)
    incorrect = html2text(incorrect)
    
    #aggiungo handler per ricevere aggiornamenti sul quiz in corso
    #riga commentata per quando in futuro sarà possibile ricevere update anche sui quiz
    #client.add_handler(PollHandler(callback=check_trivial_updates))

    client.add_handler(RawUpdateHandler(callback=check_trivial_updates))
    
    try:
        msg = client.send_poll(get_chat(message),question="Category: " + category.title() + "\nDifficulty: " + difficulty.title() + "\n" + question,options=incorrect,type=PollType.QUIZ,correct_option_id=incorrect.index(correct),open_period=20,is_anonymous=False,reply_to_message_id=get_id_msg(message))
        
        #aggiungo su db dati sul trivial in corso
        save_trivial_data(get_chat(message),msg.id,difficulty.title(),category.title(),tipo_domanda[question_type].title())

    except errors.exceptions.bad_request_400.PollAnswersInvalid:
        return sendMessage(client,message,"__Errore durante invio trivial__")


punteggi = { 'Easy'  : 1,
             'Medium': 2,
             'Hard'  : 3}

"""
    Funzione che prende raw updates per ogni volta che un giocatore vota sul quiz, assegnando o meno il punteggio.
"""
@Client.on_raw_update()
def check_trivial_updates(client,update,users,chat):
    if isinstance(update,UpdateMessagePollVote):
        data = update
        player = data.user_id
        chosen = data.options[0]
        int_chosen = int.from_bytes(chosen,"big")
        query = get_trivial_data()
        for item in query:
            polldata = client.get_messages(item.id_chat,item.id_msg)
            if (int(polldata.poll.id) == int(data.poll_id)) and (int(int_chosen) == int(polldata.poll.correct_option_id)):
                print(str(player) + " ha risposto correttamente")
                if item.qtype == 'Boolean':
                    update_trivial_score(player,1,item.category,client,update)
                else:
                    update_trivial_score(player,punteggi[item.diff],item.category,client,update)
            elif polldata.poll.is_closed:
                delete_trivial_data(item.id_msg)

"""
    richiamo funzione per punteggi personali
"""
def get_personal_score(_,client,message):
    return personal_trivial_leaderboard(get_id_user(message),client,message)

"""
    richiamo funzione per classifica globale
"""
def get_global_score(query,client,message):
    for item in categorie:
        if query.title() in item:
            query = item
    return global_trivial_leaderboard_category(query,client,message)

