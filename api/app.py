from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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
