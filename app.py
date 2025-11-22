from fastapi import FastAPI
import uuid
import uvicorn
import json
import os

app = FastAPI()

# simple JSON files in the project folder
BASE_DIR = os.path.dirname(__file__)
CARDS_FILE = os.path.join(BASE_DIR, "cards.json")
TRIPS_FILE = os.path.join(BASE_DIR, "trips.json")

# in-memory sets
cards = set()
trips = set()


def _load(path: str, store: set):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                store.update(data)
        except Exception:
            # keep it simple for demo: ignore malformed file
            pass


def _save(path: str, store: set):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(list(store), f)
    except Exception:
        pass


# load persisted data on startup (if present)
_load(CARDS_FILE, cards)
_load(TRIPS_FILE, trips)


@app.get("/ping")
def ping():
    return {"msg": "pong"}


@app.get('/generate_card')
def generate_card():
    id_str = str(uuid.uuid4())
    cards.add(id_str)
    _save(CARDS_FILE, cards)
    return {"id": id_str}


@app.get('/cards')
def list_cards():
    return {"cards": sorted(list(cards))}


@app.get('/generate_trip')
def generate_trip():
    id_str = str(uuid.uuid4())
    trips.add(id_str)
    _save(TRIPS_FILE, trips)
    return {"id": id_str}


@app.get('/trips')
def list_trips():
    return {"trips": sorted(list(trips))}


if __name__ == "__main__":
    # Start the ASGI server when running `python app.py` directly
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)