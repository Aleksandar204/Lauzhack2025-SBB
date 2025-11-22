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
trips = {}
# key je trip_id
# value je origin, dest, timestamp, type
#setuje se tako sto dobijemo VALUE i izmislimo KEY
#checkuje se tako sto dobijemo KEY i vratimo VALUE
#nema delete, nema update


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
_load(TRIPS_FILE, trips)


@app.get("/ping")
def ping():
    return {"msg": "pong"}

@app.get('/check')
def check_trip(trip_id: str, controllor_id: str):
    #not yet implemented: checking copied cards which are scanned by the same controllor_id
    if trip_id in trips:
        return {"found": True, "details": trips[trip_id]}
    else:
        return {"found": False}


@app.post('/generate_trip')
def generate_trip(origin: str, destination: str, trip_type: str, timestamp: str):
    id_str = str(uuid.uuid4())
    trips[id_str] = {"origin": origin, "destination": destination, "timestamp": timestamp, "type": trip_type}
    _save(TRIPS_FILE, trips)
    return {"id": id_str}




# @app.get('/trips')
# def list_trips():
#     return {"trips": sorted(list(trips))}


if __name__ == "__main__":
    # Start the ASGI server when running `python app.py` directly
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)