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

def main():
    bulbasaur = Pokemon(1,
                        "Bulbasaur",
                        "grass",
                        "poison",
                        None,
                        2)

if __name__ == "__main__":
    main()