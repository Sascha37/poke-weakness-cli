# Poke Weakness Display CLI

# About
A python script that returns a nice visual respresentation of type weaknesses of a chosen Pokemon.

![Screenshot 1](/screenshots/ss1.png)
# Requirements
You need to have Python installed and the following libraries: 
```
pip install requests
```

# How to run
```
python pokeweaknesscli.py 
```

# Known Issues
When running on Windows:
- identifiers scirpt fails to generate json file
- cant open files because Windows file paths uses '\' instead of '/'
- ANSI escape color codes dont work when ran in Windows CMD

# Credits
- PokeAPI https://pokeapi.co
- Pokemon identifiers script https://github.com/acxz/pokeshell/blob/master/scripts/create_pokemon_identifiers.py

