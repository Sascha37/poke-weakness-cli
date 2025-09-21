#!/usr/bin/env python3

import urllib.request
import json
import colorama
from pathlib import Path
import poke_identifiers

# Needed for ANSI Escape codes to work on Windows Command Line
colorama.just_fix_windows_console()

scriptlocation = Path(__file__).parent

class colors:
    NAME = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Reference: https://bulbapedia.bulbagarden.net/wiki/Help:Color_templates
    BUG = '\x1b[38;2;145;161;25m'
    DARK = '\x1b[38;2;153;139;140m' # Using the light version of the color for readability
    DRAGON = '\x1b[38;2;80;96;225m'
    ELECTRIC = '\x1b[38;2;250;192;0m'
    FAIRY = '\x1b[38;2;239;112;239m'
    FIGHTING = '\x1b[38;2;255;128;0m'
    FIRE = '\x1b[38;2;230;40;41m'
    FLYING = '\x1b[38;2;129;185;239m'
    GHOST = '\x1b[38;2;112;65;112m'
    GRASS = '\x1b[38;2;63;161;41m'
    GROUND = '\x1b[38;2;145;81;33m'
    ICE = '\x1b[38;2;61;206;243m'
    NORMAL = '\x1b[38;2;159;161;159m'
    POISON = '\x1b[38;2;145;65;203m'
    PSYCHIC = '\x1b[38;2;239;65;121m'
    ROCK = '\x1b[38;2;175;169;129m'
    STEEL = '\x1b[38;2;96;161;184m'
    WATER = '\x1b[38;2;41;128;239m'

try:
    with open(scriptlocation  / 'pokemon_identifiers.json', encoding="utf-8") as fp:
        pokemon_identifier = json.load(fp)
except FileNotFoundError:
    print("Missing identifiers file. This is normal if you are running the script for the first time.")
    print("Press Enter to generate (this action will take around 1-2 Minutes)")

    try:
        input()
    except KeyboardInterrupt:
        print("\nExiting...")
        exit(0)

    poke_identifiers.generate()
    with open(scriptlocation  / 'pokemon_identifiers.json', encoding="utf-8") as fp:
        pokemon_identifier = json.load(fp)

def colorizeType(type):
    type_colors = {
        "bug": colors.BUG,
        "dark": colors.DARK,
        "dragon": colors.DRAGON,
        "electric": colors.ELECTRIC,
        "fairy": colors.FAIRY,
        "fighting": colors.FIGHTING,
        "fire": colors.FIRE,
        "flying": colors.FLYING,
        "ghost": colors.GHOST,
        "grass": colors.GRASS,
        "ground": colors.GROUND,
        "ice": colors.ICE,
        "normal": colors.NORMAL,
        "poison": colors.POISON,
        "psychic": colors.PSYCHIC,
        "rock": colors.ROCK,
        "steel": colors.STEEL,
        "water": colors.WATER
        }
    return colors.BOLD + type_colors.get(type, "") + type.upper() + colors.ENDC


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
    print("━"*40)
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
    print("━"*40)
