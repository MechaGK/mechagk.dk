"""Main module for my website"""
import markdown
import os
from flask import Flask, render_template, Markup, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, '/tmp/mechagk.dk.db'),
))

app.config.from_envvar('MECHAGK_DK_SETTINGS', silent=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{app.config['DATABASE']}"
db = SQLAlchemy(app)


class BalkonenSheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(1024), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    study = db.Column(db.String(256), nullable=False)
    occupation = db.Column(db.String(256), nullable=False)
    second_occupation = db.Column(db.String(256), nullable=True)
    third_occupation = db.Column(db.String(256), nullable=True)
    fun_fact = db.Column(db.String(512), nullable=False)


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


@app.route('/balkonen-sheet/<sheet_id>', methods=['GET'])
def view_balkonen_sheet(sheet_id):
    sheet = BalkonenSheet.query.filter_by(id=sheet_id).first_or_404()
    return render_template('balkonen_template.html',
                           image_url=sheet.image_url,
                           name=sheet.name, occupation=sheet.occupation,
                           study=sheet.study, fun_fact=sheet.fun_fact)


@app.route('/balkonen-template', methods=['GET', 'POST'])
def balkonen_template_create():
    if request.method == 'POST':
        data = request.get_json() or request.values
        sheet = BalkonenSheet(
            image_url=data.get('imageUrl',
                               'https://geppel.dk/wp-content/uploads/2014/10/kaj-beanbag.jpg'),
            name=data.get('name', 'Kaj'),
            occupation=data.get('occupation', 'Underholdning'),
            study=data.get('study', 'Popcorn'),
            fun_fact=data.get('funFact', 'insert joke')
        )

        db.session.add(sheet)
        db.session.commit()

        return redirect(url_for('view_balkonen_sheet', sheet_id=sheet.id))
    else:
        return render_template('balkonen_generator.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
