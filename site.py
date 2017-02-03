"""Main module for my website"""
from flask import Flask, render_template
from flaskext.markdown import Markdown
import json
app = Flask(__name__)
Markdown(app)


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
        games_list = []

        game_data = {}
        for key, value in games.items():
            game_data = value
            value["shortName"] = key
            games_list.append(game_data)

        chunks = []
        current_chunk = []
        for i in range(len(games_list)):
            current_chunk.append(games_list[i])

            if i % 2 == 1:
                chunks.append(current_chunk)
                current_chunk = []

        if len(current_chunk) > 0:
            chunks.append(current_chunk)

        return render_template('games.html', games=chunks)
    else:
        if game in games:
            game_data = games[game]
            game_data['shortName'] = game

            page_file = open(f"descriptions/{game}.md", 'r')
            game_data['description'] = page_file.read()

            return render_template(
                'game.html', games=games, game_data=game_data)
        else:
            return render_template(
                'games.html', games=games, error='not-found')
