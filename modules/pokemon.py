from utils.get_config import sendMessage,sendPhoto
from pyrogram import Client,errors
import pokebase
import random

"""
    Restituisce informazioni sul pokemon richiesto
"""

def get_pokemon_info(query,client,message):
    sendMessage(client,message,"__Looking for " + query.title() + " in pokedex...__")
    # Ottieni informazioni sul Pokémon
    pokemon = pokebase.pokemon(query.lower())

    # Ottieni informazioni aggiuntive
    species = pokebase.pokemon_species(pokemon.id)
    abilities = [ability.ability.name for ability in pokemon.abilities]

    # Estrai casualmente 5 mosse
    all_moves = [move.move.name for move in pokemon.moves]
    moves = random.sample(all_moves, min(5, len(all_moves)))

    # Costruisci un dizionario con le informazioni
    pokemon_info = {
        'name': pokemon.name,
        'image_url': pokemon.sprites.front_default,
        'height': pokemon.height / 10.0,  # Converti l'altezza da decimetri a metri
        'generation': species.generation.name.capitalize(),
        'pokedex_number': pokemon.id,
        'abilities': abilities,
        'moves': moves,
    }

    # Aggiungi la descrizione se presente
    if species.flavor_text_entries:
        for entry in species.flavor_text_entries:
            if entry.language.name == 'en':  # Filtra le descrizioni in inglese
                pokemon_info['description'] = entry.flavor_text
            break
    result =  "Informazioni su **{}**: ".format(pokemon_info['name'].title())
    result += "\nAltezza: **{}** metri".format(pokemon_info['height'])
    result += "\nGenerazione: **{}**".format(pokemon_info['generation'])
    result += "\nNumero nel Pokédex: **{}**".format(pokemon_info['pokedex_number'])
    result += "\nAbilità: **{}**".format(', '.join(pokemon_info['abilities']))
    result += "\nAlcune mosse: **{}**".format(', '.join(pokemon_info['moves']))
    if 'description' in pokemon_info:
        result += "\nDescrizione: __{}__".format(pokemon_info['description'])
    else:
        result +="\n__Descrizione non disponibile.__"
    #restituisco lo sprite e come caption le info del pokemon
    return sendPhoto(client,message,pokemon_info['image_url'],result)
