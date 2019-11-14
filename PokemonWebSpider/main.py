import argparse
import scrapper
from pokemons import PokemonStorage
import random
from webgenerator import create_team_page


def create_pokedex(args):
    print("Create the pokedex")
    PokemonStorage.clean_database()
    pokemons = scrapper.get_pokedex(not args.no_cache)
    PokemonStorage.store_pokemons(pokemons.keys(), pokemons.values())
    print(f"Stored {len(pokemons)} pokemons")

    print(PokemonStorage.get_pokemon(133).all_related)


def get_team(args):
    print("Getting a team of 6 pokemons")
    team = list()
    current_types = set()

    type_pairs = PokemonStorage.get_type_pairs(exclude_none=True)
    random.shuffle(type_pairs)

    while len(team) < 6:
        type1, type2 = type_pairs.pop()
        if type1 in current_types or type2 in current_types:
            continue

        pokemons = PokemonStorage.get_pokemons_with_types(type1, type2)
        team.append(random.choice(pokemons))
        current_types.update((type1, type2))

    create_team_page(team)


def main(args):
    if args.command == "create-pokedex":
        create_pokedex(args)
    else:
        get_team(args)


def create_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_create_pokedex = subparsers.add_parser("create-pokedex")
    parser_create_pokedex.add_argument("--no-cache", action="store_true")

    parser_get_team = subparsers.add_parser("get-team")

    return parser

if __name__ == "__main__":
    args = create_parser().parse_args()
    main(args)