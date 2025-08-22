#!/usr/bin/env python3

import urllib.request
import json
from pathlib import Path
import identifiers

scriptlocation = Path(__file__).parent

class colors:
    NAME = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

    RED = '\x1b[38;5;9m'
    GREEN = '\x1b[38;5;10m'
    YELLOW = '\x1b[38;5;11m'
    DARKWHITE = '\x1b[38;5;15m'
    GRAY = '\x1b[38;5;7m'
    ROCKGRAY = '\x1b[38;5;249m'
    STEELGRAY = '\x1b[38;5;255m'
    FAIRYPINK = '\x1b[38;5;13m'
    PSYCHICPINK = '\x1b[38;5;212m'
    PURPLE = '\x1b[38;5;98m'
    GHOSTPURPLE = '\x1b[38;5;141m'
    DARKGREEN = '\x1b[38;5;107m'
    BLUE = '\x1b[38;5;45m'
    ICEBLUE = '\x1b[38;5;14m'
    DRAGONBLUE = '\x1b[38;5;69m'
    FLYINGBLUE = '\x1b[38;5;153m'
    ORANGE = '\x1b[38;5;214m'
    BROWN = '\x1b[38;5;178m'
    BLACK = '\x1b[38;5;241m'

try:
    with open(str(scriptlocation) + '/pokemon_identifiers.json') as fp:
        pokemon_identifier = json.load(fp)
except FileNotFoundError:
    print("Missing identifiers file. This is normal if you are running the script for the first time.")
    print("Press Enter to generate (this action will take around 50 seconds)")

    try:
        input()
    except KeyboardInterrupt:
        print("\nExiting...")
        exit(0)

    identifiers.generate()
    with open(str(scriptlocation) + '/pokemon_identifiers.json') as fp:
        pokemon_identifier = json.load(fp)

def colorizeType(type):
    match type:
        case "normal":
            return colors.BOLD + colors.GRAY + type.upper() + colors.ENDC
        case "fire":
            return colors.BOLD + colors.RED + type.upper() + colors.ENDC
        case "water":
            return colors.BOLD + colors.BLUE + type.upper() + colors.ENDC
        case "electric":
            return colors.BOLD + colors.YELLOW + type.upper() + colors.ENDC
        case "grass":
            return colors.BOLD + colors.GREEN + type.upper() + colors.ENDC
        case "ice":
            return colors.BOLD + colors.ICEBLUE + type.upper() + colors.ENDC
        case "fighting":
            return colors.BOLD + colors.ORANGE + type.upper() + colors.ENDC
        case "poison":
            return  colors.BOLD + colors.PURPLE + type.upper() + colors.ENDC
        case "ground":
            return colors.BOLD + colors.BROWN + type.upper() + colors.ENDC
        case "flying":
            return colors.BOLD + colors.FLYINGBLUE + type.upper() + colors.ENDC
        case "psychic":
            return colors.BOLD + colors.PSYCHICPINK + type.upper() + colors.ENDC
        case "bug":
            return  colors.BOLD + colors.DARKGREEN + type.upper() + colors.ENDC
        case "rock":
            return colors.BOLD + colors.ROCKGRAY + type.upper() + colors.ENDC
        case "ghost":
            return colors.BOLD + colors.GHOSTPURPLE + type.upper() + colors.ENDC
        case "dragon":
            return colors.BOLD + colors.DRAGONBLUE + type.upper() + colors.ENDC
        case "dark":
            return colors.BOLD + colors.BLACK + type.upper() + colors.ENDC
        case "steel":
            return colors.BOLD + colors.STEELGRAY + type.upper() + colors.ENDC
        case "fairy":
            return colors.BOLD + colors.FAIRYPINK + type.upper() + colors.ENDC
        case _:
            return colors.BOLD + type.upper() + colors.ENDC

while(True):
    print("Ctrl + C to exit.")
    # Taking input
    while(True):
        try:
            input_pokemon = input(colors.NAME + colors.BOLD +"Enter Pokemon to display its weaknesses:" + colors.ENDC).lower()
            pokemon = pokemon_identifier[input_pokemon]
        except KeyError:
            print("Invalid name")
            continue
        except KeyboardInterrupt:
            print("\nExiting...")
            exit(0)
        break
    try:
        rawhttps = urllib.request.urlopen("https://pokeapi.co/api/v2/pokemon/" + pokemon).read()
    except:
        print("pokeapi.co could not be reached. please check your network settings")
        exit(1)

    data = json.loads(rawhttps)

    types = [t["type"]["name"] for t in data["types"]]
    english_name= data["species"]["name"]
    multipliers = {}
    for t in types:
        try:
            raw_type_data = urllib.request.urlopen("https://pokeapi.co/api/v2/type/" + t).read()
        except:
            print("pokeapi.co could not be reached. please check your network settings")
            exit(1)

        type_data = json.loads(raw_type_data)
        damage_relations = type_data["damage_relations"]

        # Double damage
        for doubledamagetype in damage_relations["double_damage_from"]:
            name = doubledamagetype["name"]
            multipliers[name] = multipliers.get(name, 1) * 2

        # Half damage
        for halfdamagetype in damage_relations["half_damage_from"]:
            name = halfdamagetype["name"]
            multipliers[name] = multipliers.get(name, 1) * 0.5

        # No damage
        for nodamagetype in damage_relations["no_damage_from"]:
            name = nodamagetype["name"]
            multipliers[name] = 0

    weaknesses4 = {k: v for k, v in multipliers.items() if v == 4}
    weaknesses2 = {k: v for k, v in multipliers.items() if 4 > v > 1}
    resistances = {k: v for k, v in multipliers.items() if 0 < v < 1}
    immunities = {k: v for k, v in multipliers.items() if v == 0}


    # Fancy Output
    print("------------------------------------")
    print(colors.NAME + colors.BOLD + english_name.capitalize() + colors.ENDC, end = " - ")
    for t in types:
        print(colorizeType(t),end=" ")
    print(end="\n")
    print(end="\n")
    print("Weaknesses (x4): ", end = "")
    if weaknesses4:
        for key in weaknesses4:
            print(colorizeType(key), end = " ")
    else: print("None",end = "")
    print(end="\n")

    print("Weaknesses (x2): ", end = "")
    if weaknesses2:
        for key in weaknesses2:
            print(colorizeType(key), end = " ")
    else: print("None",end = "")
    print(end="\n")

    print("Resistances:     ", end = "")
    if resistances:
        for key in resistances:
            print(colorizeType(key), end = " ")
    else: print("None",end = "")
    print(end="\n")

    print("Immunities:      ", end = "")
    if immunities:
        for key in immunities:
            print(colorizeType(key), end = " ")
    else: print("None",end = "")
    print(end="\n")
    print("------------------------------------")
