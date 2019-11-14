# Reto Pokémon Web Spider <img src="https://image.flaticon.com/icons/svg/1752/1752813.svg" alt="Snorlax" height="40" width="40"> <img src="https://image.flaticon.com/icons/svg/1752/1752867.svg" alt="Teddiursa" height="40" width="40"> <img src="https://image.flaticon.com/icons/svg/1752/1752682.svg" alt="Duskull" height="40" width="40"> <img src="https://image.flaticon.com/icons/svg/1752/1752713.svg" alt="Jigglypuff" height="40" width="40"> <img src="https://image.flaticon.com/icons/svg/1752/1752633.svg" alt="Aaron" height="40" width="40"> <img src="https://image.flaticon.com/icons/svg/1752/1752695.svg" alt="Gloom" height="40" width="40">
El 2n reto antes de la Hackeps 2019, consistirá en un pokémon scrapper que tendrá que mostrar los resultados en formato html (se valorará la presentación). 
En las siguientes secciones dispondrás de la información de forma detallada:

## <img src="https://image.flaticon.com/icons/svg/1934/1934019.svg" alt="Explanation Icon" height="40" width="40"> Explicación del Reto
En las siguientes secciones se explicarán el reto, los conocimientos que se consideran esenciales para afrontarlo y algunos enlaces útiles para llevarlo a cabo.

### <img src="https://image.flaticon.com/icons/svg/1180/1180260.svg" alt="Explanation Icon" height="40" width="40"> Explicación
Este reto consiste en conseguir crear un equipo de 6 pokémon de doble tipo (planta/agua, fuego/eléctrico) sin que se repita ninguno. Además, para realizarlo, tenéis que buscar en el html de la pokémonDB y mostrar los 6 pokémon (sprite, tipos, número de pokédex y nombre).

Cómo RESTRICCIÓN addicional, no se pueden poner pokémon de la misma cadena evolutiva, por ejemplo, se puede poner a eevee, pero entonces todas sus evoluciones quedan descartadas (eevee, flareon, vaporeon, jolteon...).

# Usage
The proposed solution has two steps:

1. Scrap the pokedex website to generate a database with pokemons.
2. Using this database, create the team while banning (1) types and (2) pokemons
from the same evolution chain.

To create the pokedex use:
```
$ python main.py create-pokedex [--no-cache]
```

To generate a team use:
```
$ python main.py get-team [--seed SEED]
```

To generate the _html_ file, use:
```
$ python main.py get-team --html [--seed SEED]
```

[The generated _html_](team.html) was created using the seed 1234.