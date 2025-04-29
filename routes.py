import io
import csv
from flask import Blueprint, jsonify, request, send_file
from config import Config
from services.pokeapi_client import get_pokemon, get_pokemon_type
from models import Pokemon, PokemonType
from database import db
from utils import write_new_pokemon

api = Blueprint("api", __name__, url_prefix="/api/pokemon")


def get_or_create_type(type_name: str):
    pokemon_type = PokemonType.query.filter_by(name=type_name).first()
    if pokemon_type:
        return pokemon_type

    type_data = get_pokemon_type(type_name)
    if not type_data:
        return None

    pokemon_type = PokemonType(name=type_data["name"])
    db.session.add(pokemon_type)
    db.session.commit()
    return pokemon_type


@api.route("/fetch", methods=["POST"])
def fetch_all():
    """
    Fetch all Pokémon data and store them
    """
    cfg = Config()
    created = []

    for raw_name in cfg.POKEMON_LIST:
        name = raw_name.lower()
        data = get_pokemon(raw_name)
        if not data:
            continue

        pokemon = Pokemon.query.filter_by(name=name).first()
        if not pokemon:
            pokemon = Pokemon(
                name=name,
                base_experience=data["base_experience"],
                height=data["height"],
                weight=data["weight"],
            )
            db.session.add(pokemon)
            db.session.flush()
            created.append(pokemon.to_dict())

            # Add types
            pokemon.types.clear()
            for tinfo in data["types"]:
                type_name = tinfo["type"]["name"]
                t = get_or_create_type(type_name)
                pokemon.types.append(t)

    if created:
        db.session.commit()

    return jsonify({"created": True}), 200


@api.route("/", methods=["GET"])
def list_all():
    """
    List all Pokémon in the database.
    """
    pokemons = Pokemon.query.all()
    return jsonify([p.to_dict() for p in pokemons]), 200


@api.route("/<string:name>", methods=["GET"])
def get_one(name: str):
    """
    Get a specific Pokémon by name.
    """
    pokemon = Pokemon.query.filter_by(name=name.lower()).first()
    if not pokemon:
        return jsonify({"error": "Pokemon not found"}), 404
    return jsonify(pokemon.to_dict()), 200


@api.route("/add/<string:name>", methods=["POST"])
def add_one(name: str):
    """
    Add a specific Pokémon by name and update config.yaml.
    """
    name_lower = name.lower()
    data = get_pokemon(name)
    if not data:
        return jsonify({"error": "Pokemon not found"}), 404

    pokemon = Pokemon.query.filter_by(name=name_lower).first()
    status = 200
    if not pokemon:
        pokemon = Pokemon(
            name=name_lower,
            base_experience=data["base_experience"],
            height=data["height"],
            weight=data["weight"],
        )
        db.session.add(pokemon)
        write_new_pokemon(name_lower)

        # Add types
        pokemon.types.clear()
        for tinfo in data["types"]:
            type_name = tinfo["type"]["name"]
            t = get_or_create_type(type_name)
            pokemon.types.append(t)

        db.session.commit()
        status = 201

    return jsonify(pokemon.to_dict()), status


@api.route("/export", methods=["GET"])
def export_all():
    """
    Export all Pokémon to CSV or JSON format.
    """
    pokemons = Pokemon.query.all()
    fmt = request.args.get("format", "json").lower()
    if fmt == "csv":
        si = io.StringIO()
        writer = csv.writer(si)
        if pokemons:
            header = ["id", "name", "base_experience", "height", "weight", "types"]
            writer.writerow(header)
            for p in pokemons:
                type_names = ",".join([t.name for t in p.types])
                row = [p.id, p.name, p.base_experience, p.height, p.weight, type_names]
                writer.writerow(row)
        output = io.BytesIO(si.getvalue().encode())
        return send_file(
            output,
            mimetype="text/csv",
            as_attachment=True,
            download_name="pokemons.csv",
        )
    return jsonify([p.to_dict() for p in pokemons]), 200
