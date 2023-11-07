[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=MasterCruelty_robbot&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=MasterCruelty_robbot)
[![Quality Gate Pass](https://sonarcloud.io/api/project_badges/measure?project=MasterCruelty_robbot&metric=alert_status)](https://sonarcloud.io/dashboard?id=MasterCruelty_robbot)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=MasterCruelty_robbot&metric=ncloc)](https://sonarcloud.io/dashboard?id=MasterCruelty_robbot)
![License](https://img.shields.io/github/license/MasterCruelty/robbot)
[![image](https://img.shields.io/github/stars/MasterCruelty/robbot)](https://github.com/MasterCruelty/robbot/stargazers)
[![image](https://img.shields.io/github/forks/MasterCruelty/robbot)](https://github.com/MasterCruelty/robbot/network/members)
![CodeSize](https://img.shields.io/github/languages/code-size/MasterCruelty/robbot)
[![image](https://img.shields.io/github/issues/MasterCruelty/robbot)](https://github.com/MasterCruelty/robbot/issues)
![image](https://img.shields.io/github/languages/top/MasterCruelty/robbot)
![image](https://img.shields.io/github/commit-activity/w/MasterCruelty/robbot)
![Image](https://badgen.net/github/release/MasterCruelty/robbot?label=Latest%20release)
![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/MasterCruelty/robbot/latest?color=44CC11&style=flat-square)
![image](https://img.shields.io/github/contributors/MasterCruelty/robbot)

# Robbot
**IT/ENG**

#### <i>This Telegram bot has the same structure of this [project](https://github.com/MasterCruelty/my-tg-app) which is an userbot I made for several features I needed.<br>So this bot has some commands in common with that userbot but also other new commands and obviously there aren't those commands that a bot can't execute but a userbot can. <br> So if you're interested you can also visit that repository.</i>

** **
# <b>Feel free to contribute and improve the project. <br> See more details on How to contribute [here](https://github.com/MasterCruelty/robbot/blob/master/CONTRIBUTING.md).<br>
After the Italian section you will find an english version of the README. In <code>doc</code> folder you will find a bit of documentation of RobBot.</b>

# **[IT]**

# Come impostare

Per un corretto funzionamento è necessario compilare a dovere il file ```config.json```. Quindi è necessario essere in possesso dei seguenti dati:

* Api keys di Telegram: ```api_id``` e ```api_hash```. Puoi generarle da [qui](https://my.telegram.org/apps)
* Bot token: ```bot_token```. Puoi generarlo da [qui](https://t.me/BotFather)
* Api url atm se si vogliono usare le loro api: ```api_url``` e ```api_get```. (Non essendo pubbliche non le condividerò)
* Api key di OpenWeatherMap: ```api_weather```. Puoi generare la tua key dal sito principale di [OpenWeatherMap](https://openweathermap.org/)
* Api di OpenAI: ```api_openai```. Puoi generare la tua key dal sito principale di [OpenAI](https://www.openai.com)
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
* registrare un nuovo gruppo come unico autorizzato a ricevere un certo comando: `/setgroup` <id_gruppo> <comando>
* cancellare un gruppo salvato: `/delgroup` <id_gruppo>
* mostrare tutti i gruppi salvati: `/listgroup`
* modificare un valore nelle statistiche di un utente per un certo comando: `/updatestat` <id_utente> 'comando' <nuovo_valore>
* cancellare un comando dalle statistiche di un utente: `/delstat` <id_utente> 'comando'
* Aggiornare i dati Telegram di un utente(nome e username): `/updaterobuser` <id_utente> (oppure dando lo username)
* Aggiornare il credito di un utente per l'utilizzo di openai: `/amount` <id_utente> <valore>
* Visualizzare l'elenco degli utenti che hanno del credito di utilizzo per openai: `/allamounts`
* Riavviare il bot direttamente da Telegram senza passare dalla shell: `/restart`
* Inviare un messaggio a un utente registrato: `/say` <username> ; 'messaggio'

### Dipendenze

* Pyrogram
* geopy
* bs4
* wikipedia
* pandas
* openai
* urbandictionary
* pdf2image
* pytube
* flightradar24
* FlightRadarAPI

### Progetti esterni usati

* [Pyrogram](https://github.com/pyrogram/pyrogram)
* [OpenWeatherMap](https://openweathermap.org/)
* [Covid19 dati Italiani sui casi](https://github.com/pcm-dpc/COVID-19)
* [Covid19 dati Italiani sui vaccini](https://github.com/italia/covid19-opendata-vaccini)
* [Geopy](https://github.com/geopy/geopy)
* [Wikipedia wrapper](https://github.com/goldsmith/Wikipedia)
* [Peewee](https://github.com/coleifer/peewee)
* [wttr.in](https://github.com/chubin/wttr.in)
* [OpenAI](https://www.openai.com)
* [Urban Dictionary](https://www.github.com/bocong/urbandictionary-py)
* [Tper open data](https://solweb.tper.it/web/tools/open-data/open-data.aspx)
* [TrainMonitor per le API viaggiatreno](https://github.com/bluviolin/TrainMonitor) (Queste API non sono pubbliche, non abusate del servizio)
* [Trenitalia-API di SimoDax per le API frecce.it](https://github.com/SimoDax/Trenitalia-API) (Queste API non sono pubbliche, non abusate del servizio)
* [Piste Kart Italia(scraping)](https://www.pistekartitalia.it)
* [Open Trivia Database](https://opentdb.com/)
* [Sito pmi.it per calcolo stipendio netto in Italia(scraping)](https://www.pmi.it/servizi/292472/calcolo-stipendio-netto.html)
* [Api Mathjs](http://api.mathjs.org)
* [The cat api](https://api.thecatapi.com/v1/images/search)
* [Dog ceo api](https://dog.ceo/api/breeds/image/random)
* [Random fox api](https://randomfox.ca/floof/)
* [Free LaTeX api](https://latex.codecogs.com)
* [Free api per immagini randomiche](https://source.unsplash.com)
* [Sito web di Passport Index(scraping)](https://www.passportindex.org/)
* [Bollettini criticita idrogeologica di open data Sicilia](https://github.com/opendatasicilia/DPC-bollettini-criticita-idrogeologica-idraulica)
* [Dati sui comuni italiani di open data Sicilia](https://github.com/opendatasicilia/comuni-italiani)
* [Nasa apod API](https://github.com/nasa/apod-api)
* [BGG API](https://boardgamegeek.com/wiki/page/BGG_XML_API2)
* [flightradar24](https://github.com/mkorkmaz/flightradar24)
* [FlightRadarAPI](https://github.com/JeanExtreme002/FlightRadarAPI)
* [Joke API](https://sv443.net/jokeapi/v2/)

# **[ENG]**

# How to setup

The correct way to setup this bot is to compile the file  ```config.json```. So it's necessary to have these data:

* Telegram api keys: ```api_id``` e ```api_hash```. You can generate them [here](https://my.telegram.org/apps)
* Telegram bot token: ```bot_token```. You can generate it from [here](https://t.me/BotFather)
* Atm api url if you wanna use their api: ```api_url``` e ```api_get```. (The api are not public so I won't share them here)
* OpenWeatherMap api key: ```api_weather```. You can generate your key from the [OpenWeatherMap website.](https://openweathermap.org/)
* OpenAI api key: ```api_openai```. You can generate your key from the [OpenAI](https://www.openai.com) website.
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
* Save a new group to make it the only one authorized to receive a specific command: `/setgroup` <id_group> <command>
* Delete a saved group: `/delgroup` <id_group>
* Show all saved groups: `/listgroup`
* Update a value in a user's stat for a specific command: `/updatestat` <id_user> 'command' <new_value>
* Delete a command from a user's stat: `/delstat` <id_user> 'command'
* Update user's Telergam data(name and username): `/updaterobuser` <id_user> (or giving username)
* Update the user's credit for openai usage: `/amount` <id_user> <value>
* Show all user and their openai credit: `/allamounts`
* Restarting the bot directly in Telegram without manually doing in shell: `/restart`
* Sending a message to a registered user: `/say` <id_user> ; 'message'


### Dependencies

* Pyrogram
* geopy
* bs4
* wikipedia
* pandas
* openai
* urbandictionary
* pdf2image
* pytube
* flightradar24
* FlightRadarAPI


### External projects used

* [Pyrogram](https://github.com/pyrogram/pyrogram)
* [OpenWeatherMap](https://openweathermap.org/)
* [Covid19 cases Italian data](https://github.com/pcm-dpc/COVID-19)
* [Covid19 vaccine Italian data](https://github.com/italia/covid19-opendata-vaccini)
* [Geopy](https://github.com/geopy/geopy)
* [Wikipedia wrapper](https://github.com/goldsmith/Wikipedia)
* [Peewee](https://github.com/coleifer/peewee)
* [wttr.in](https://github.com/chubin/wttr.in)
* [OpenAI](https://www.openai.com)
* [Urban Dictionary](https://www.github.com/bocong/urbandictionary-py)
* [Tper open data](https://solweb.tper.it/web/tools/open-data/open-data.aspx)
* [TrainMonitor for viaggiatreno API](https://github.com/bluviolin/TrainMonitor) (These API aren't public, don't abuse the service)
* [SimoDax's wiki for frecce.it API](https://github.com/SimoDax/Trenitalia-API)  (These API aren't public, don't abuse the service)
* [Piste Kart Italia(scraping)](https://www.pistekartitalia.it)
* [Open Trivia Database](https://opentdb.com/)
* [pmi.it website to calculate Italian net salary(scraping)](https://www.pmi.it/servizi/292472/calcolo-stipendio-netto.html)
* [Api Mathjs](http://api.mathjs.org)
* [The cat api](https://api.thecatapi.com/v1/images/search)
* [Dog ceo api](https://dog.ceo/api/breeds/image/random)
* [Random fox api](https://randomfox.ca/floof/)
* [Free LaTeX api](https://latex.codecogs.com)
* [Free api for random images](https://source.unsplash.com)
* [Passport Index Web Site(scraping)](https://www.passportindex.org/)
* [Open data about extreme forecast event by open data Sicilia](https://github.com/opendatasicilia/DPC-bollettini-criticita-idrogeologica-idraulica)
* [Open data about italian municipalities by Open data Sicilia](https://github.com/opendatasicilia/comuni-italiani)
* [Nasa apod API](https://github.com/nasa/apod-api)
* [BGG API](https://boardgamegeek.com/wiki/page/BGG_XML_API2)
* [flightradar24](https://github.com/mkorkmaz/flightradar24)
* [FlightRadarAPI](https://github.com/JeanExtreme002/FlightRadarAPI)
* [Joke API](https://sv443.net/jokeapi/v2/)
