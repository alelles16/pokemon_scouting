import os
import yaml


def write_new_pokemon(name: str) -> None:
    """
    Write a new Pokémon name to the YAML configuration file.
    Args:
        name (str): The name of the Pokémon to add.
    """
    config_path = os.path.join(os.getcwd(), "pokemon_list.yml")
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
        if name not in cfg["pokemon_list"]:
            cfg["pokemon_list"].append(name)
            cfg["pokemon_list"].sort()
            with open(config_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(cfg, f, sort_keys=False, allow_unicode=True)
