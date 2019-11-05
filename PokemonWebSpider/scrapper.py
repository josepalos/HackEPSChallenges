#/usr/bin/env python3.7
from pokemons import Pokemon, PokemonStorage

import requests
from requests.exceptions import Timeout, ReadTimeout, ConnectionError
import requests_cache
from bs4 import BeautifulSoup
from typing import Tuple, List
import functools
import time
import sys

MAX_DELAY_REQUESTS = 5


requests_cache.install_cache("pokemons_cache", expire_after=24*60*60)


def get_throttled(url):
    delay = 0
    while True:
        try:
            response = requests.get(url, timeout=(5, 10))
            return response
        except (Timeout, ReadTimeout, ConnectionError):
            sys.stderr.write("Timeout, delay\n")
            delay = min(delay + 1, MAX_DELAY_REQUESTS)


POKEDEX_BASE_URL = "https://pokemondb.net"
POKEDEX_URL = "{}/pokedex/national".format(POKEDEX_BASE_URL)


def get_pokemon_number(infocard) -> bool:
    infocard_id = infocard.find("small").text
    return int(infocard_id.replace("#", ""))


def scrap_evolutions(number: int, pokemon_url: str) -> Tuple[int, List[int]]:
    # Example of evolution information:
    # <div class="infocard-list-evo">
    #   <div class="infocard ">
    #       <span class="infocard-lg-img"><a href="/pokedex/bulbasaur"><img class="img-fixed img-sprite" src="https://img.pokemondb.net/sprites/omega-ruby-alpha-sapphire/dex/normal/bulbasaur.png" alt="Bulbasaur sprite"></a></span>
    #       <span class="infocard-lg-data text-muted">
    #           <small>#001</small>
    #           <br><a class="ent-name" href="/pokedex/bulbasaur">Bulbasaur</a><br><small><a href="/type/grass" class="itype grass">Grass</a> · <a href="/type/poison" class="itype poison">Poison</a></small>
    #       </span>
    #   </div>
    #   <span class="infocard infocard-arrow"><i class="icon-arrow icon-arrow-e"></i><small>(Level 16)</small></span>
    #   <div class="infocard ">
    #       <span class="infocard-lg-img"><a href="/pokedex/ivysaur"><img class="img-fixed img-sprite" src="https://img.pokemondb.net/sprites/omega-ruby-alpha-sapphire/dex/normal/ivysaur.png" alt="Ivysaur sprite"></a></span>
    #       <span class="infocard-lg-data text-muted">
    #           <small>#002</small>
    #           <br><a class="ent-name" href="/pokedex/ivysaur">Ivysaur</a><br> <small><a href="/type/grass" class="itype grass">Grass</a> · <a href="/type/poison" class="itype poison">Poison</a></small>
    #       </span>
    #   </div>
    #   <span class="infocard infocard-arrow"><i class="icon-arrow icon-arrow-e"></i><small>(Level 32)</small></span>
    #   <div class="infocard ">
    #       <span class="infocard-lg-img"><a href="/pokedex/venusaur"><img class="img-fixed img-sprite" src="https://img.pokemondb.net/sprites/omega-ruby-alpha-sapphire/dex/normal/venusaur.png" alt="Venusaur sprite"></a></span>
    #       <span class="infocard-lg-data text-muted">
    #           <small>#003</small>
    #           <br><a class="ent-name" href="/pokedex/venusaur">Venusaur</a><br> <small><a href="/type/grass" class="itype grass">Grass</a> · <a href="/type/poison" class="itype poison">Poison</a></small>
    #       </span>
    #   </div>
    # </div>
    url = "{}{}".format(POKEDEX_BASE_URL, pokemon_url)
    data = get_throttled(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    evolution_infocards = soup.find_all(class_="infocard-list-evo")
    
    related_pokemons = set()
    for infocard in evolution_infocards:
        related_pokemons_infocards = infocard.find_all(class_="infocard-lg-data")
        related_ids = [get_pokemon_number(related) for related in related_pokemons_infocards]
        related_pokemons.update(related_ids)
    
    return list(related_pokemons)
    

def parse_infocard(infocard):
    # Example of infocard:
    # <span class="infocard-lg-data text-muted">
    #   <small>#001</small>
    #   <br>
    #   <a class="ent-name" href="/pokedex/bulbasaur">Bulbasaur</a><br>
    #   <small>
    #       <a href="/type/grass" class="itype grass">Grass</a>
    #       ·
    #       <a href="/type/poison" class="itype poison">Poison</a>
    #   </small>
    # </span>

    print("New pokemon")

    text_data = infocard.find(class_="infocard-lg-data")
    smalls = text_data.find_all("small")

    number = int(smalls[0].text.replace("#", ""))
    print("Parsing pokemon %d" % number)
    name = text_data.a.text
    types_data = smalls[1].find_all('a')
    type1 = types_data[0].text
    try:
        type2 = types_data[1].text
    except IndexError:
        # This pokemon only has one type
        type2 = None

    pokemon_url = text_data.a["href"]

    evolution_related_pokemons = scrap_evolutions(number, pokemon_url)

    return Pokemon(number, name, type1, type2, evolution_related_pokemons)

def retrieve_pokedex():
    data = get_throttled(POKEDEX_URL)
    soup = BeautifulSoup(data.text, 'html.parser')
    infocards = soup.find_all(class_="infocard")

    return (parse_infocard(infocard) for infocard in infocards)

def main():
    # PokemonStorage.store_pokemons([
    #     Pokemon(1, "Bulbasaur", "grass", "poison", None, 2),
    #     Pokemon(2, "Ivysaur", "grass", "poison", 1, 3),
    #     Pokemon(3, "Venusaur", "grass", "poison", 2, 3),
    # ])
    # print(PokemonStorage.get_pokemon(2))

    PokemonStorage.store_pokemons(retrieve_pokedex())
    evee = PokemonStorage.get_pokemon(133)

    for pokemon_id in evee.evolution_related_pokemons:
        try:
            print(PokemonStorage.get_pokemon(pokemon_id))
        except KeyError:
            print("[MISSING] %d" % pokemon_id)

    umbreon = PokemonStorage.get_pokemon(197)
    for pokemon_id in evee.evolution_related_pokemons:
        try:
            print(PokemonStorage.get_pokemon(pokemon_id))
        except KeyError:
            print("[MISSING] %d" % pokemon_id)

    

if __name__ == "__main__":
    main()