# Poke Weakness Display CLI

# About
A python script that returns a nice visual respresentation of type weaknesses of a chosen Pokemon.
You can search Pokemon by their English name, NatDex ID number, or by their names in different languages.

![Screenshot 1](/screenshots/ss1.png)
# Requirements
## Arch Linux
```
sudo pacman -S python python-colorama python-requests
```
## Windows
You need to have Python installed and the following libraries: 
```
pip install requests
pip install colorama
```

# How to run
Start the Terminal or Command Line in the folder where the script is located and run:
```
python poke-weakness-cli.py 
```

# TODO
- [ ] fuzzy matching to allow for typos while searching Pokemon

# Credits
- PokeAPI https://pokeapi.co
- Pokemon identifiers script https://github.com/acxz/pokeshell/blob/master/scripts/create_pokemon_identifiers.py
