from pokemons import Pokemon
from typing import List
import webbrowser

BOOTSTRAP_STYLESHEET = '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">'

def create_team_page(team: List[Pokemon], output_file="team.html"):
    content = '<div class="row">'
    for pokemon in team:
        content += f"""
        <div class="col-sm-4">
            <div class="card">
                <img src="{pokemon.sprite_url}" class="card-img-top" />
                <div class="card-body">
                    <h5 class="card-title">#{pokemon.number} - {pokemon.name} </h5>
                    <p class="card-text">{pokemon.type1} / {pokemon.type2} </p>
                </div>
            </div>
        </div>
        """

    web_page = f"""
    <html>
        <head>
            {BOOTSTRAP_STYLESHEET}
        </head>
        <body>
            <div class="container">
                <div class="row">
                    {content}
                </div>
            </div>
        </body>
    </html>
    """

    with open(output_file, "w") as f:
        f.write(web_page)

    webbrowser.open(output_file)