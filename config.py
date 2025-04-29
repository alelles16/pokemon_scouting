import yaml
import os


class Config:
    def __init__(self):
        # Set database URI
        with open("config.yml", "r", encoding="utf-8") as f:
            cfg_db = yaml.safe_load(f)

        cwd = os.getcwd()
        database_name = f"{cfg_db['database']['db_name']}.db"
        self.SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(cwd, database_name)}"

        # Set Pokémon list
        with open("pokemon_list.yml", "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)

        self.POKEMON_LIST = cfg["pokemon_list"]
