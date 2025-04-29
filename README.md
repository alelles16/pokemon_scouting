# Pokémon Scouting Data

A Python application that retrieves data from the PokeAPI, processes it, stores it in SQLite, and provides REST endpoints to fetch, add, list, and export Pokémon information.

## Features
- **Fetch**: Retrieves Pokémon data from the PokeAPI and stores it in the database.
- **List**: Lists all Pokémon currently stored.
- **Get**: Retrieves a specific Pokémon by name.
- **Add**: Adds a new Pokémon and updates the configuration file.
- **Export**: Exports data in JSON or CSV format.
- **Swagger / OpenAPI**: Interactive API documentation available at `/apidocs/`.

## Project Structure
```bash
pokemon_scout_app/
├── app.py              # Entry point; initializes Flask, Swagger, and database
├── config.py           # Loads configuration (pokemon list, DB URI)
├── database.py         # Sets up SQLAlchemy
├── models.py           # ORM models: Pokemon and PokemonType
├── routes.py           # REST endpoints definition
├── services/           # Business logic and PokeAPI client
│   └── pokeapi_client.py
├── utils.py            # Helper functions (e.g. write_new_pokemon)
├── config.yaml         # Pokémon list and database URI
├── requirements.txt    # Python dependencies
├── swagger.yaml        # External OpenAPI specification
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose setup
└── tests/              # pytest end-to-end tests
    └── test_api.py
```  

## Requirements
- Python 3.11 or higher
- pip / virtualenv
- Docker & Docker Compose (optional)

## Local Setup & Running
1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/pokemon-scouting.git
   cd pokemon_scout_app
   ```
2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set environment variables**
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development    # or production
   ```
5. **Run the application**
   ```bash
   flask run --host=0.0.0.0 --port=5001
   ```
6. **Open in browser**
   - Base API: `http://localhost:5001/api/pokemon/`
   - Swagger UI: `http://localhost:5001/apidocs/`

## Configuring for Additional Pokémon
Edit the **`config.yaml`** file to include new Pokémon names:
```yaml
pokemon_list:
  - Pikachu
  - Charizard
  - NewPokemon  # add more here

database:
  uri: sqlite:///pokemon.db
```
Save and restart the app. A `POST /api/pokemon/fetch` will process any newly added names.

## Running with Docker
1. **Build and start services**
   ```bash
   docker-compose up --build
   ```
2. **Access the API & docs**
   - `http://localhost:5001/api/pokemon/`
   - `http://localhost:5001/apidocs/`

## Testing
Run the test suite with:
```bash
pytest
```

## Additional Resources
- **Swagger / OpenAPI** spec: `swagger.yaml`  
- **Database file**: `pokemon.db` (ignored in git)  
- **Utility scripts**: see `utils.py` for helper functions
