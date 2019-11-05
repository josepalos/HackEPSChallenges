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
    evolution_related_pokemons: List[int]

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
