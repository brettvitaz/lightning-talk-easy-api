from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from api.import_data import import_from_file

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokedex.sqlite'

db = SQLAlchemy(app)


class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    stamina = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    cp_max = db.Column(db.Integer)
    category = db.Column(db.String)

    types = db.relationship('Type', secondary='pokemon_type')


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)


class PokemonType(db.Model):
    pokemon_id = db.Column(db.Integer, db.ForeignKey(Pokemon.id), primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey(Type.id), primary_key=True)


db.create_all()

import_from_file(db, Pokemon)
import_from_file(db, Type)
import_from_file(db, PokemonType)

ma = Marshmallow(app)


class PokemonSchema(ma.ModelSchema):
    types = ma.Nested('TypeSchema', many=True)

    class Meta:
        model = Pokemon


class TypeSchema(ma.ModelSchema):
    class Meta:
        model = Type


@app.route('/api/pokemon')
def route_pokemon():
    pokemon_schema = PokemonSchema(many=True)
    all_pokemon = Pokemon.query.all()
    return pokemon_schema.jsonify(all_pokemon)


@app.route('/api/pokemon/<int:pokemon_id>')
def route_pokemon_id(pokemon_id):
    pokemon_schema = PokemonSchema()
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    return pokemon_schema.jsonify(pokemon)


@app.route('/api/pokemon/page/<int:page>')
def route_pokemon_page(page):
    pokemon_schema = PokemonSchema(many=True)
    all_pokemon = Pokemon.query.paginate(page=page, per_page=10)
    return pokemon_schema.jsonify(all_pokemon.items)


if __name__ == '__main__':
    app.run(debug=True)
