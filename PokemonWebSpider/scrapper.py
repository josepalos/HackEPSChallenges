#/usr/bin/env python3.7
from dataclasses import dataclass
from typing import List


@dataclass
class Pokemon:
    number: int
    name: str
    type1: str
    type2: str
    # sprite: TODO
    # Evolution chain is represented by identifiers, not the pokemon object itself.
    evolves_from: int
    evolves_to: List[int]

    def __repr__(self):
        return "Pokemon [{}, {}]".format(self.number, self.name)


class PokemonStorage:
    _pokemons = dict()
    @classmethod
    def store_pokemon(cls, pokemon: Pokemon):
        cls._pokemons[pokemon.number] = pokemon

    @classmethod
    def store_pokemons(cls, pokemons: List[Pokemon]):
        for pokemon in pokemons:
            cls.store_pokemon(pokemon)

    @classmethod
    def get_pokemon(cls, identifier: int) -> Pokemon:
        return cls._pokemons[identifier]


def main():
    PokemonStorage.store_pokemons([
        Pokemon(1, "Bulbasaur", "grass", "poison", None, 2),
        Pokemon(2, "Ivysaur", "grass", "poison", 1, 3),
        Pokemon(3, "Venusaur", "grass", "poison", 2, 3),
    ])

    print(PokemonStorage.get_pokemon(2))

if __name__ == "__main__":
    main()