from fastapi import FastAPI
import uuid
import uvicorn
import json
import os

app = FastAPI()

# simple JSON files in the project folder
TRIPS_FILE = "trips.json"

# in-memory dict: key = trip_id, value = origin, dest, timestamp, type
trips = {}
# key je trip_id
# value je origin, dest, timestamp, type
#setuje se tako sto dobijemo VALUE i izmislimo KEY
#checkuje se tako sto dobijemo KEY i vratimo VALUE
#nema delete, nema update


def _load(path: str, store: dict):
    path = 'server/'+path
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(data)
            # Prefer persisted dict mapping {trip_id: details}
            if isinstance(data, dict):
                store.clear()
                store.update(data)
                print(data)
                print(store)
                print("!!!")
            # If older format was a list, try to convert common list shapes
            elif isinstance(data, list):
                pass
                # converted = {}
                # for item in data:
                #     if not isinstance(item, dict):
                #         continue
                #     # shape 1: {'id': '<uuid>', ...details...}
                #     if 'id' in item and isinstance(item['id'], str):
                #         item_copy = dict(item)
                #         id_val = item_copy.pop('id')
                #         converted[id_val] = item_copy
                #         continue
                #     # shape 2: [{'<id>': {...}} , ...]
                #     if len(item) == 1:
                #         k = next(iter(item))
                #         if isinstance(k, str):
                #             converted[k] = item[k]
                # if converted:
                #     store.clear()
                #     store.update(converted)
        except Exception:
            # keep it simple for demo: ignore malformed file
            print("Failed to load trips file")


def _save(path: str, store: dict):
    path = 'server/'+path

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(store, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# load persisted data on startup (if present)
_load(TRIPS_FILE, trips)
print(TRIPS_FILE)
print(trips)

@app.get("/ping")
def ping():
    return {"msg": "pong"}

@app.get('/check')
def check_trip(trip_id: str, controllor_id: str):
    print(trip_id)
    print(trips)


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