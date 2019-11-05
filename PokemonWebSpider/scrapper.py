#/usr/bin/env python3.7
from pokemons import Pokemon, PokemonStorage

def main():
    PokemonStorage.store_pokemons([
        Pokemon(1, "Bulbasaur", "grass", "poison", None, 2),
        Pokemon(2, "Ivysaur", "grass", "poison", 1, 3),
        Pokemon(3, "Venusaur", "grass", "poison", 2, 3),
    ])

    print(PokemonStorage.get_pokemon(2))

if __name__ == "__main__":
    main()