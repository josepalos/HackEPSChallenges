from dataclasses import dataclass
from typing import List
import json
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("sqlite:///pokemons.sqlite")
database_filename = "pokemons.sqlite"
Base = declarative_base()
Session = sessionmaker(bind = engine)


class Pokemon(Base):
    __tablename__ = "pokemons"

    number = Column(Integer, primary_key=True)
    name = Column(String)
    type1 = Column(String)
    type2 = Column(String)
    sprite_url = Column(String)
    # Evolution chain is represented by identifiers, not the pokemon object itself.
    #evolution_related_pokemons: List[int]

    def __repr__(self):
        return "Pokemon [{}, {}]".format(self.number, self.name)


Base.metadata.create_all(engine)


class PokemonStorage:
    @classmethod
    def clean_database(cls):
        session = Session()
        session.query(Pokemon).delete()
        session.commit()

    @classmethod
    def store_pokemon(cls, pokemon: Pokemon):
        cls.store_pokemons([pokemon])

    @classmethod
    def store_pokemons(cls, pokemons: List[Pokemon]):
        session = Session()
        session.add_all(pokemons)
        session.commit()

    @classmethod
    def get_pokemon_count(cls):
        session = Session()
        return session.query(Pokemon).count()

    @classmethod
    def get_pokemon(cls, number: int) -> Pokemon:
        session = Session()
        return session.query(Pokemon).get(number)
