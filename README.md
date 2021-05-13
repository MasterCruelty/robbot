![License](https://img.shields.io/github/license/MasterCruelty/robbot)
[![image](https://img.shields.io/github/stars/MasterCruelty/robbot)](https://github.com/MasterCruelty/robbot/stargazers)
[![image](https://img.shields.io/github/forks/MasterCruelty/robbot)](https://github.com/MasterCruelty/robbot/network/members)
![CodeSize](https://img.shields.io/github/languages/code-size/MasterCruelty/robbot)
[![image](https://img.shields.io/github/issues/MasterCruelty/robbot)](https://github.com/MasterCruelty/robbot/issues)
![image](https://img.shields.io/github/languages/top/MasterCruelty/robbot)
![image](https://img.shields.io/github/commit-activity/w/MasterCruelty/robbot)

# Robbot
**IT/ENG**


# **[IT]**

# Come impostare

Per un corretto funzionamento è necessario compilare a dovere il file ```config.json```. Quindi è necessario essere in possesso dei seguenti dati:

* Api keys di Telegram: ```api_id``` e ```api_hash```.
* Bot token: ```bot_token```.
* Api url atm se si vogliono usare le loro api: ```api_url``` e ```api_get```.
* Api key di OpenWeatherMap: ```api_weather```.
* I dati telegram dell'amministratore del bot: ```id_super_admin```.
* Il percorso dove si trova il file .db: ```path_db```.
* Nome della sessione: ```session_name```.
* I nomi dei comandi utente, admin e superadmin: ```user_commands```, ```admin_commands``` e ```super_admin_commands```.

I dati del super admin servono a colui che potrà usare le funzioni di interazione con il database e altre funzioni particolari.
I nomi dei comandi da inserire nel ```config.json``` possono essere ricopiati dal codice oppure possono essere modificati sul codice e poi ricopiati nel file json.	

### Dipendenze

* Pyrogram
* geopy
* bs4
* wikipedia


# **[ENG]**

# How to setup

The correct way to setup this bot is to compile the file  ```config.json```. So it's necessary to have these data:

* Telegram api keys: ```api_id``` e ```api_hash```.
* Telegram bot token: ```bot_token```.
* Atm api url if you wanna use their api: ```api_url``` e ```api_get```.
* OpenWeatherMap api key: ```api_weather```.
* Telegram data of the owner of the bot: ```id_super_admin```.
* The path where is the .db file: ```path_db```.
* The session name: ```session_name```.
* Name of user commands, admin commands and super admin commands: ```user_commands```, ```admin_commands``` e ```super_admin_commands```.

Data of super admin is needed because he's the only one who can use db functions and other special functions.
Name of commands to put inside ```config.json``` can be copied from source code or renamed inside source code and then copied in json file.	

### Dependencies

* Pyrogram
* geopy
* bs4
* wikipedia
