from utils.get_config import sendMessage,sendPhoto
from pyrogram import Client,errors
import pokebase
import requests
import json
import random

"""
    Restituisce informazioni sul pokemon richiesto
"""

def get_pokemon_info(query,client,message):
    sendMessage(client,message,"__Looking for " + query.title() + " in pokedex...__")
    # Ottieni informazioni sul Pokémon
    pokemon = pokebase.pokemon(query.lower())
    # Ottieni informazioni aggiuntive
    try:
        species = pokebase.pokemon_species(pokemon.id)
    except AttributeError:
        return sendMessage(client,message,"__No pokémon found.__")
    abilities = [ability.ability.name for ability in pokemon.abilities]
    location_urls = [encounter.location_area.url for encounter in pokemon.location_area_encounters]
    types_name = [item.type.name for item in pokemon.types]
    weight = pokemon.weight / 10
    #Estrai 5 località casuali dove è possibile trovare il pokémon
    location_urls_extracted = random.sample(location_urls,min(5,len(location_urls)))
    loc_names = []
    for url in location_urls_extracted:
        resp = requests.get(url)
        loc_data = json.loads(resp.text)
        loc_names.append(loc_data['name'])

    # Estrai casualmente 5 mosse
    all_moves = [move.move.name for move in pokemon.moves]
    moves = random.sample(all_moves, min(5, len(all_moves)))

    # Costruisci un dizionario con le informazioni
    pokemon_info = {
        'name': pokemon.name,
        'type': types_name,
        'weight': weight,
        'image_url': pokemon.sprites.front_default,
        'height': pokemon.height / 10.0,  # Converti l'altezza da decimetri a metri
        'generation': species.generation.name.capitalize(),
        'pokedex_number': pokemon.id,
        'abilities': abilities,
        'moves': moves,
        'locations': loc_names,
    }

    # Aggiungi la descrizione se presente
    if species.flavor_text_entries:
        for entry in species.flavor_text_entries:
            if entry.language.name == 'en':  # Filtra le descrizioni in inglese
                pokemon_info['description'] = entry.flavor_text
            break
    result =  "Informazioni su **{}**: ".format(pokemon_info['name'].title())
    result += "\nTipo: **{}** ".format(', '.join(pokemon_info['type']))
    result += "\nPeso: **{}** kg".format(weight)
    result += "\nAltezza: **{}** metri".format(pokemon_info['height'])
    result += "\nGenerazione: **{}**".format(pokemon_info['generation'])
    result += "\nNumero nel Pokédex: **{}**".format(pokemon_info['pokedex_number'])
    result += "\n\nAbilità: **{}**".format(', '.join(pokemon_info['abilities']))
    result += "\n\nAlcune mosse: **{}**".format(', '.join(pokemon_info['moves']))
    result += "\n\nAlcune località: **{}**".format(', '.join(pokemon_info['locations']))
    if 'description' in pokemon_info:
        result += "\nDescrizione: __{}__".format(pokemon_info['description'])
    else:
        result +="\n__Descrizione non disponibile.__"
    #restituisco lo sprite e come caption le info del pokemon
    return sendPhoto(client,message,pokemon_info['image_url'],result)
