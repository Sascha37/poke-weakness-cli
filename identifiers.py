#!/usr/bin/env python

# this is a modified script. original script from: github.com/acxz/pokeshell/blob/master/scripts/create_pokemon_identifiers.py

# Script to create a mapping between various identifiers for the same pokemon

import requests
import json
from pathlib import Path
scriptlocation = Path(__file__).parent

def generate():
    print("Obtaining pokemon identifiers...")

    # Grab total number of pokemon species to iterate over
    pokemon_species_endpoint_limited = "https://pokeapi.co/api/v2/pokemon-species"
    pokemon_species_response_limited = requests.get(pokemon_species_endpoint_limited)
    pokemon_species_response_limited_json = pokemon_species_response_limited.json()
    pokemon_species_count = pokemon_species_response_limited_json['count']

    # Get all pokemon species
    pokemon_species_endpoint = "https://pokeapi.co/api/v2/pokemon-species?limit=" + str(pokemon_species_count)
    pokemon_species_response = requests.get(pokemon_species_endpoint)
    pokemon_species_response_json = pokemon_species_response.json()
    pokemon_species_results = pokemon_species_response_json['results']

    # For each pokemon species, grab all identifiable names
    pokemon_identifiers = {}
    for pokemon_species_result_idx in range(pokemon_species_count):

        # Obtain each species' response
        pokemon_species_idx_endpoint = pokemon_species_results[pokemon_species_result_idx]['url']
        pokemon_species_idx_response = requests.get(pokemon_species_idx_endpoint)
        pokemon_species_idx_response_json = pokemon_species_idx_response.json()

        # Grab the canonical name for each pokemon species
        pokemon_species_idx_name = pokemon_species_idx_response_json['name']

        # Grab the id for each pokemon species
        pokemon_species_idx_id = pokemon_species_idx_response_json['id']
        dexnumber = str(pokemon_species_idx_id)
        # TODO: format this with indentation and overwriting the previous line
        print(str(pokemon_species_idx_name) + ": " + dexnumber)

        # Add the id as an identifier
        pokemon_identifiers |= {pokemon_species_idx_id: dexnumber}

        # Add the canonical name as an identifier
        pokemon_identifiers |= {pokemon_species_idx_name: dexnumber}

        # Grab the localized names for each pokemon species
        pokemon_species_idx_names = pokemon_species_idx_response_json['names'][:-1]
        # The last entry is not a name, hence the `[:-1]`
        names = pokemon_species_idx_names[:-1]
        for name_idx in range(len(names)):
            name = pokemon_species_idx_names[name_idx]['name']
            name = name.casefold()
            pokemon_identifiers |= {name: dexnumber}

    pokemon_identifiers |= {"シキジカ-あき": "deerling-autumn"}

    print("Obtained pokemon identifiers.")
    with open(scriptlocation  / 'pokemon_identifiers.json', "w", encoding="utf-8") as json_file:
        json.dump(pokemon_identifiers, json_file, ensure_ascii = False, indent = 2)
