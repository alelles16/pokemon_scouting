from database import db


pokemon_types = db.Table(
    "pokemon_types",
    db.Column("pokemon_id", db.Integer, db.ForeignKey("pokemon.id"), primary_key=True),
    db.Column("type_id", db.Integer, db.ForeignKey("pokemontype.id"), primary_key=True),
)


class Pokemon(db.Model):
    __tablename__ = "pokemon"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    base_experience = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)

    types = db.relationship(
        "PokemonType", secondary=pokemon_types, back_populates="pokemons"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "base_experience": self.base_experience,
            "height": self.height,
            "weight": self.weight,
            "types": [type.to_dict() for type in self.types],
        }


class PokemonType(db.Model):
    __tablename__ = "pokemontype"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    pokemons = db.relationship(
        "Pokemon", secondary=pokemon_types, back_populates="types"
    )

    def to_dict(self):
        return {"id": self.id, "name": self.name}
