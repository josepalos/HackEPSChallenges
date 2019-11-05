import argparse
import scrapper
from pokemons import PokemonStorage
import random

def main(args):
    if args.command == "create-pokedex":
        print("Create the pokedex")
        pokemons = scrapper.get_pokedex(not args.no_cache)
        PokemonStorage.store_pokemons(pokemons)
        PokemonStorage.save()
        print(f"Stored {len(pokemons)} pokemons")
    else:
        print("Getting a team of 6 pokemons")
        PokemonStorage.init()
        for i in range(0, 6):
            pokemon_id = random.randint(1, PokemonStorage.get_pokemon_count() + 1)
            print(PokemonStorage.get_pokemon(pokemon_id))


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