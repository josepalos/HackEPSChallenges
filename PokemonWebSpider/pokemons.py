from dataclasses import dataclass
from typing import List, Tuple
import json
from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey, select
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("sqlite:///pokemons.sqlite")
database_filename = "pokemons.sqlite"
Base = declarative_base()
Session = sessionmaker(bind = engine)

# Evolution self-relation explained in:
# https://stackoverflow.com/a/9119764
evolution_chain = Table(
    "evolution_chain",
    Base.metadata,
    Column("pokemon1", Integer, ForeignKey("pokemons.number"), primary_key=True),
    Column("pokemon2", Integer, ForeignKey("pokemons.number"), primary_key=True)
)


class Pokemon(Base):
    __tablename__ = "pokemons"

    number = Column(Integer, primary_key=True)
    name = Column(String)
    type1 = Column(String)
    type2 = Column(String)
    sprite_url = Column(String)
    related = relationship("Pokemon",
                secondary=evolution_chain,
                primaryjoin=number == evolution_chain.c.pokemon1,
                secondaryjoin=number == evolution_chain.c.pokemon2)

    def __repr__(self):
        return "Pokemon [{}, {}]".format(self.number, self.name)

# Viewonly relationship that selects across all the related pokemons.
chain_union = select([
    evolution_chain.c.pokemon1,
    evolution_chain.c.pokemon2
]).union(
    select([
        evolution_chain.c.pokemon2,
        evolution_chain.c.pokemon1
    ])
).alias()

Pokemon.all_related = relationship("Pokemon",
                        secondary=chain_union,
                        primaryjoin=Pokemon.number == chain_union.c.pokemon1,
                        secondaryjoin=Pokemon.number == chain_union.c.pokemon2,
                        viewonly=True)


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

    @classmethod
    def get_pokemons_with_types(cls, type1, type2) -> List[Pokemon]:
        session = Session()
        l1 = session.query(Pokemon).filter(Pokemon.type1 == type1, Pokemon.type2 == type2).all()
        l2 = session.query(Pokemon).filter(Pokemon.type1 == type2, Pokemon.type2 == type1).all()

        return list(set((*l1, *l2)))

    @classmethod
    def get_type_pairs(cls, exclude_none=False) -> List[Tuple[str, str]]:
        session = Session()
        query = session.query(Pokemon.type1, Pokemon.type2)
        if exclude_none:
            query = query.filter(Pokemon.type1 != None, Pokemon.type2 != None)
        return list(set(query.all()))
   