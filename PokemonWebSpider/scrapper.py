#/usr/bin/env python3.7
import multiprocessing
import time
import sys

from typing import Tuple, List, Dict

import requests
import requests.exceptions
import requests_cache
from bs4 import BeautifulSoup

from pokemons import Pokemon

MAX_DELAY_REQUESTS = 5
DEFAULT_PROCESSES = 20


requests_cache.install_cache("pokemons_cache", expire_after=24*60*60)


def get_throttled(url: str) -> BeautifulSoup:
    delay = 0
    while True:
        try:
            response = requests.get(url, timeout=(5, 10))
            return response
        except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectionError):
            sys.stderr.write("Timeout, delay\n")
            delay = min(delay + 1, MAX_DELAY_REQUESTS)


POKEDEX_BASE_URL = "https://pokemondb.net"
POKEDEX_URL = "{}/pokedex/national".format(POKEDEX_BASE_URL)


def get_pokemon_number(infocard: BeautifulSoup) -> int:
    infocard_id = infocard.find("small").text
    return int(infocard_id.replace("#", ""))


def scrap_evolutions(pokemon_url: str) -> List[int]:
    url = "{}{}".format(POKEDEX_BASE_URL, pokemon_url)
    data = get_throttled(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    evolution_infocards = soup.find_all(class_="infocard-list-evo")

    related_pokemons = set()
    for infocard in evolution_infocards:
        related_infocards = infocard.find_all(class_="infocard-lg-data")
        related_ids = [get_pokemon_number(related)
                       for related in related_infocards]
        related_pokemons.update(related_ids)

    return list(related_pokemons)


def parse_infocard(infocard: BeautifulSoup) -> Tuple[Pokemon, List[int]]:
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

    pokemon = Pokemon(number=number, name=name, type1=type1, type2=type2,
                      sprite_url=image_url)
    evolution_related_pokemons = scrap_evolutions(pokemon_url)

    return pokemon, evolution_related_pokemons


def prune_bs_tree(element: BeautifulSoup) -> BeautifulSoup:
    return BeautifulSoup(str(element), 'html.parser')


def get_pokedex(cache: bool = True,
                processes: int = DEFAULT_PROCESSES
                ) -> Dict[Pokemon, List[int]]:
    """
    Returns a dictionary where the keys are all the pokemons and the values are
    the list of related pokemons.
    """
    if not cache:
        print("Removing cache")
        requests_cache.clear()
    else:
        print("Using cache")

    data = get_throttled(POKEDEX_URL)
    soup = BeautifulSoup(data.text, 'html.parser')
    infocards = soup.find_all(class_="infocard")

    # Prune the tree because multiprocessing needs to pickle the data,
    # and passing the original elements cause RecursionError
    infocards_pruned = (prune_bs_tree(infocard) for infocard in infocards)

    with multiprocessing.Pool(processes) as pool:
        parsed = pool.map(parse_infocard, infocards_pruned)

    return dict(parsed)

if __name__ == "__main__":
    start = time.time()
    get_pokedex()
    end = time.time()
    print(end - start)
