[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=MasterCruelty_robbot&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=MasterCruelty_robbot)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=MasterCruelty_robbot&metric=ncloc)](https://sonarcloud.io/dashboard?id=MasterCruelty_robbot)
![License](https://img.shields.io/github/license/MasterCruelty/robbot)
[![image](https://img.shields.io/github/stars/MasterCruelty/robbot)](https://github.com/MasterCruelty/robbot/stargazers)
[![image](https://img.shields.io/github/forks/MasterCruelty/robbot)](https://github.com/MasterCruelty/robbot/network/members)
![CodeSize](https://img.shields.io/github/languages/code-size/MasterCruelty/robbot)
[![image](https://img.shields.io/github/issues/MasterCruelty/robbot)](https://github.com/MasterCruelty/robbot/issues)
![image](https://img.shields.io/github/languages/top/MasterCruelty/robbot)
![image](https://img.shields.io/github/commit-activity/w/MasterCruelty/robbot)
![image](https://img.shields.io/github/contributors/MasterCruelty/robbot)

# Robbot
**IT/ENG**

#### <i>This Telegram bot has the same structure of this [project](https://github.com/MasterCruelty/my-tg-app) which is an userbot I made for several features I needed.<br>So this bot has some commands in common with that userbot but also other new commands and obviously there aren't those commands that a bot can't execute but a userbot can. <br> So if you're interested you can also visit that repository.</i>

# **[IT]**

# Come impostare

Per un corretto funzionamento è necessario compilare a dovere il file ```config.json```. Quindi è necessario essere in possesso dei seguenti dati:

* Api keys di Telegram: ```api_id``` e ```api_hash```. Puoi generarle da [qui](https://my.telegram.org/apps)
* Bot token: ```bot_token```. Puoi generarlo da [qui](https://t.me/BotFather)
* Api url atm se si vogliono usare le loro api: ```api_url``` e ```api_get```. (Non essendo pubbliche non le condividerò)
* Api key di OpenWeatherMap: ```api_weather```. Puoi generare la tua key dal sito principale di OpenWeatherMap
* I dati telegram dell'amministratore del bot: ```id_super_admin```.
* Il percorso dove si trova il file .db: ```path_db```.
* Nome della sessione: ```session_name```.
* I nomi dei comandi utente, admin e superadmin: ```user_commands```, ```admin_commands``` e ```super_admin_commands```.

I dati del super admin servono a colui che potrà usare le funzioni di interazione con il database e altre funzioni particolari.
I nomi dei comandi da inserire nel ```config.json``` possono essere ricopiati dal codice oppure possono essere modificati sul codice e poi ricopiati nel file json.	

### Come funzionano i comandi utente del bot

Il funzionamento dei comandi utente è spiegato all'interno del file ```help.json```. Si tratta del file che viene usato dal bot per rispondere al comando ```/helprob <nome comando>```.
Le spiegazioni sono in Italiano, ma volendo si possono tradurre in qualsiasi lingua sostituendo i campi della struttura dati oppure addirittura renderlo multilingua, ma in quel caso c'è da sviluppare la componente che rende possibile il cambio di lingua.

### Come funzionano i comandi admin e super

* registrare un nuovo utente: ```/setrobuser``` <id_utente>
* registrare un nuovo admin: ```/setrobadmin``` <id_utente> 
* cancellare un utente: ```/delrobuser``` <id_utente>
* revocare i privilegi admin: ```/delrobadmin``` <id_utente> (l'utente sarà comunque ancora tra i registrati ma senza i poteri admin)
* mostrare tutti gli utenti registrati: ```/listrobuser```
* mostrare il numero di utenti registrati: ```/allrobuser```
* verificare se il bot è online: ```/pingrob```

### Dipendenze

* Pyrogram
* geopy
* bs4
* wikipedia

### Progetti esterni usati

* [Pyrogram](https://github.com/pyrogram/pyrogram)
* [OpenWeatherMap](https://openweathermap.org/)
* [Covid19 dati Italiani sui casi](https://github.com/pcm-dpc/COVID-19)
* [Covid19 dati Italiani sui vaccini](https://github.com/italia/covid19-opendata-vaccini)
* [Geopy](https://github.com/geopy/geopy)
* [Wikipedia wrapper](https://github.com/goldsmith/Wikipedia)
* [Peewee](https://github.com/coleifer/peewee)
* [wttr.in](https://github.com/chubin/wttr.in)

# **[ENG]**

# How to setup

The correct way to setup this bot is to compile the file  ```config.json```. So it's necessary to have these data:

* Telegram api keys: ```api_id``` e ```api_hash```. You can generate them [here](https://my.telegram.org/apps)
* Telegram bot token: ```bot_token```. You can generate it from [here](https://t.me/BotFather)
* Atm api url if you wanna use their api: ```api_url``` e ```api_get```. (The api are not public so I won't share them here)
* OpenWeatherMap api key: ```api_weather```. You can generate your key on the main website of OpenWeatherMap
* Telegram data of the owner of the bot: ```id_super_admin```.
* The path where is the .db file: ```path_db```.
* The session name: ```session_name```.
* Name of user commands, admin commands and super admin commands: ```user_commands```, ```admin_commands``` e ```super_admin_commands```.

Data of super admin is needed because he's the only one who can use db functions and other special functions.
Name of commands to put inside ```config.json``` can be copied from source code or renamed inside source code and then copied in json file.	

### How the user bot's commands works

The features of the user commands are explained inside ```help.json```. It is the file which is used by the bot to reply at ```/helprob <command name>```.
This json file is only in Italian, but you can translate it in every languages by changing the correct fields with your translations or even making the bot multi-language but in that case you have to develop the component for change the language runtime.

### How the admin/super commands works

* register a new user: ```/setrobuser``` <id_user>
* register a new admin: ```/setrobadmin``` <id_user> 
* delete a user: ```/delrobuser``` <id_user>
* delete an admin: ```/delrobadmin``` <id_user> (it will just revoke the admin power, it doesn't delete the user)
* How to list all user registered: ```/listrobuser``` 
* How to show ho many users are registered: ```/allrobuser```
* check if the bot is online: ```/pingrob```


### Dependencies

* Pyrogram
* geopy
* bs4
* wikipedia


### External projects used

* [Pyrogram](https://github.com/pyrogram/pyrogram)
* [OpenWeatherMap](https://openweathermap.org/)
* [Covid19 cases Italian data](https://github.com/pcm-dpc/COVID-19)
* [Covid19 vaccine Italian data](https://github.com/italia/covid19-opendata-vaccini)
* [Geopy](https://github.com/geopy/geopy)
* [Wikipedia wrapper](https://github.com/goldsmith/Wikipedia)
* [Peewee](https://github.com/coleifer/peewee)
* [wttr.in](https://github.com/chubin/wttr.in)
