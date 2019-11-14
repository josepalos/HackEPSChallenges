#/usr/bin/env python3.7
from pokemons import Pokemon

import requests
from requests.exceptions import Timeout, ReadTimeout, ConnectionError
import requests_cache
from bs4 import BeautifulSoup
from typing import Tuple, List, Dict
import functools
import time
import sys

MAX_DELAY_REQUESTS = 5


requests_cache.install_cache("pokemons_cache", expire_after=24*60*60)


def get_throttled(url: str) -> BeautifulSoup:
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


def get_pokemon_number(infocard: BeautifulSoup) -> int:
    infocard_id = infocard.find("small").text
    return int(infocard_id.replace("#", ""))


def scrap_evolutions(number: int, pokemon_url: str) -> List[int]:
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
    

def parse_infocard(infocard: BeautifulSoup) -> Tuple[Pokemon, List[int]]:
    # Example of infocard:
    # <span class="infocard-lg-img">
    #   <a href="/pokedex/bulbasaur">
    #       <span class="img-fixed img-sprite"
    #             data-src="https://img.pokemondb.net/sprites/omega-ruby-alpha-sapphire/dex/normal/bulbasaur.png"
    #             data-alt="Bulbasaur sprite">
    #       </span>
    #   </a>
    # </span>
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

    image_url = infocard.find(class_="img-sprite").attrs["data-src"]

    pokemon_url = text_data.a["href"]

    pokemon = Pokemon(number=number, name=name, type1=type1, type2=type2, sprite_url=image_url)
    evolution_related_pokemons = scrap_evolutions(number, pokemon_url)

    return pokemon, evolution_related_pokemons


def get_pokedex(cache: bool=True) -> Dict[Pokemon, List[int]]:
    """
    Returns a dictionary where the keys are all the pokemons and the values are the list of related pokemons.
    """
    if not cache:
        print("Removing cache")
        requests_cache.clear()
    else:
        print("Using cache")

    data = get_throttled(POKEDEX_URL)
    soup = BeautifulSoup(data.text, 'html.parser')
    infocards = soup.find_all(class_="infocard")

    parsed = (parse_infocard(infocard) for infocard in infocards)
    return {pokemon: chain for pokemon, chain in parsed}

if __name__ == "__main__":
    import time
    start = time.time()
    get_pokedex()
    end = time.time()
    print(end - start)