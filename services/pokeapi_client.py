import requests


API_BASE = "https://pokeapi.co/api/v2"


def get_pokemon(name: str):
    url = f"{API_BASE}/pokemon/{name.lower()}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()


def get_pokemon_type(name: str):
    url = f"{API_BASE}/type/{name.lower()}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()
