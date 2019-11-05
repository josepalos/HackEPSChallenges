from dataclasses import dataclass
from typing import List
import json


@dataclass
class Pokemon:
    number: int
    name: str
    type1: str
    type2: str
    sprite_url: str
    # Evolution chain is represented by identifiers, not the pokemon object itself.
    evolution_related_pokemons: List[int]

    def __repr__(self):
        return "Pokemon [{}, {}]".format(self.number, self.name)


class PokemonJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Pokemon):
            data = obj.__dict__
            return {"_type": "pokemon", "value": data}
        return json.JSONEncoder.default(self, obj)


class PokemonJsonDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        if "_type" not in dct:
            return dct
        elif dct["_type"] == "pokemon":
            return Pokemon(**dct["value"])
        return dct

class PokemonStorage:
    database_filename = "pokemons.json"

    @classmethod
    def init(cls):
        with open(cls.database_filename, "r") as f:
            pokemons = json.load(f, cls=PokemonJsonDecoder)
            cls._pokemons = {int(k):v for k,v in pokemons.items()}

    _pokemons = dict()
    @classmethod
    def store_pokemon(cls, pokemon: Pokemon):
        cls._pokemons[pokemon.number] = pokemon

    @classmethod
    def get_pokemon_count(cls):
        return len(cls._pokemons)

    @classmethod
    def store_pokemons(cls, pokemons: List[Pokemon]):
        for pokemon in pokemons:
            cls.store_pokemon(pokemon)

    @classmethod
    def get_pokemon(cls, identifier: int) -> Pokemon:
        return cls._pokemons[identifier]

    @classmethod
    def save(cls):
        with open(cls.database_filename, "w") as f:
            json.dump(cls._pokemons, f, cls=PokemonJsonEncoder, indent=4)