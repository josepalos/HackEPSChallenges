import argparse
import random

import scrapper
from pokemons import PokemonStorage
from webgenerator import create_team_page


def create_pokedex(args):
    print("Create the pokedex")
    PokemonStorage.clean_database()
    pokemons = scrapper.get_pokedex(not args.no_cache)
    PokemonStorage.store_pokemons(pokemons.keys(), pokemons.values())
    print(f"Stored {len(pokemons)} pokemons")

    print(PokemonStorage.get_pokemon(133).all_related)


def get_random_pokemon(pokemons, banned_pokemons):
    while pokemons:
        pokemon = pokemons.pop()
        if pokemon not in banned_pokemons:
            return pokemon
    return None

def get_team(args):
    print("Getting a team of 6 pokemons")
    team = list()
    banned_types = set()
    banned_pokemons = set()

    type_pairs = PokemonStorage.get_type_pairs(exclude_none=True)
    random.shuffle(type_pairs)

    while len(team) < 6:
        type1, type2 = type_pairs.pop()
        if type1 in banned_types or type2 in banned_types:
            continue

        pokemons = PokemonStorage.get_pokemons_with_types(type1, type2)
        random.shuffle(pokemons)
        pokemon = get_random_pokemon(pokemons, banned_pokemons)
        if not pokemon:
            continue

        banned_pokemons.update(pokemon.all_related)
        team.append(pokemon)
        banned_types.update((type1, type2))

    print("TEAM")
    for pokemon in team:
        print(pokemon)

    if args.html:
        create_team_page(team)


def main():
    args = create_parser().parse_args()

    if args.command == "create-pokedex":
        create_pokedex(args)
    else:
        random.seed(args.seed)  # args.seed defaults to None
        get_team(args)


def create_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_create_pokedex = subparsers.add_parser("create-pokedex")
    parser_create_pokedex.add_argument("--no-cache", action="store_true")

    parser_get_team = subparsers.add_parser("get-team")
    parser_get_team.add_argument("--html", action="store_true")
    parser_get_team.add_argument("--seed", type=int, required=False)

    return parser


if __name__ == "__main__":
    main()
