#/usr/bin/env python3.7
from pokemons import Pokemon, PokemonStorage
import requests
from bs4 import BeautifulSoup
from typing import Tuple, List

POKEDEX_URL = "https://pokemondb.net/pokedex/national"


def scrap_evolutions(okemon_url: str) -> Tuple[int, List[int]]:
    # TODO
    return None, None


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

    text_data = infocard.find(class_="infocard-lg-data")
    smalls = text_data.find_all("small")

    number = int(smalls[0].text.replace("#", ""))
    name = text_data.a.text
    types_data = smalls[1].find_all('a')
    type1 = types_data[0].text
    try:
        type2 = types_data[1].text
    except IndexError:
        # This pokemon only has one type
        type2 = None

    pokemon_url = text_data.a["href"]

    evolves_from, evolves_to = scrap_evolutions(pokemon_url)

    return Pokemon(number, name, type1, type2, evolves_from, evolves_to)

def retrieve_pokedex():
    data = requests.get(POKEDEX_URL)
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

    pokemons = list(retrieve_pokedex())
    print(pokemons[0:5])

if __name__ == "__main__":
    main()