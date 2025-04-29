import os
import sys
import pytest
import csv
import io

dir_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, dir_root)

from app import app as flask_app
from database import db
from config import Config


@pytest.fixture(scope="module")
def app():
    flask_app.config.update(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"}
    )
    with flask_app.app_context():
        db.create_all()
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_fetch_all_creates(client):
    """
    POST /api/pokemon/fetch creates pokemons and returns 200.
    """
    rv = client.post("/api/pokemon/fetch")
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["created"] == True


def test_list_all(client):
    """
    GET /api/pokemon/ returns pokemos lists.
    """
    rv = client.get("/api/pokemon/")
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list)
    assert "name" in data[0] and "id" in data[0]


def test_get_one_success(client):
    """
    GET /api/pokemon/<existente> retorna 200 and data.
    """
    name = Config().POKEMON_LIST[0].lower()
    rv = client.get(f"/api/pokemon/{name}")
    assert rv.status_code == 200
    json = rv.get_json()
    assert json["name"] == name
    assert "types" in json and isinstance(json["types"], list)


def test_get_one_not_found(client):
    """
    GET /api/pokemon/<no_existe> returns 404.
    """
    rv = client.get("/api/pokemon/not-a-pokemon")
    assert rv.status_code == 404


def test_add_existing(client):
    """
    POST /api/pokemon/add/<existente> returns 200 y and not repeat.
    """
    existing = Config().POKEMON_LIST[0]
    rv = client.post(f"/api/pokemon/add/{existing}")
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["name"] == existing.lower()


def test_export_json(client):
    """
    GET /api/pokemon/export returns JSON.
    """
    rv = client.get("/api/pokemon/export")
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list)


def test_export_csv(client):
    """
    GET /api/pokemon/export?format=csv returns valid CSV.
    """
    rv = client.get("/api/pokemon/export?format=csv")
    assert rv.status_code == 200
    text = rv.data.decode()
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    assert rows[0] == ["id", "name", "base_experience", "height", "weight", "types"]
    for row in rows[1:]:
        assert len(row) == 6
