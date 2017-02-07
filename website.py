"""Main module for my website"""
import markdown
from flask import Flask, render_template, Markup
import json
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/games/')
@app.route('/games/<game>')
def games(game=None):
    games_file = open('games.json', 'r')
    games = json.loads(games_file.read())

    if game is None:
        return render_template('games.html', games=games)
    else:
        game_data = [g for g in games if g["shortName"] == game]

        if len(game_data) > 0:
            game_data = game_data[0]
            page_file = open(f"descriptions/{game}.md", 'r')

            description = markdown.markdown(page_file.read())
            game_data['description'] = Markup(description)

            return render_template(
                'game.html', games=games, game_data=game_data)
        else:
            return render_template(
                'games.html', games=games, error='not-found')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
