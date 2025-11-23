from fastapi import FastAPI
import uuid
import uvicorn
import json
import os

app = FastAPI()

# simple JSON files in the project folder
CARDS_FILE = "cards.json"

# in-memory dict: key = trip_id, value = origin, dest, timestamp, type
cards = {}
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
            print("Failed to load cards file")


def _save(path: str, store: dict):
    path = 'server/'+path

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(store, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


'''
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ValidationRequest(BaseModel):
    uid: str
    counter: int
    mac: str
    challenge: str
    timestamp: int

    
def validate_counter_and_mac(uid, counter, mac, challenge):
    # Placeholder for actual MAC verification logic
    cards
    return True
@app.post("/validate")
def validate_card(data: ValidationRequest):
    # Example: validate timestamp
    import time
    now = int(time.time() * 1000)


    # TODO: Put your MAC verification logic here
    if validate_counter_and_mac(data.uid, data.counter, data.mac, data.challenge):
        if abs(now - data.timestamp) > 36000000000:
            return {
                "success": False,
                "message": "Timestamp is too old"
            }
        return {
            "success": True,
            "message": "Card validated successfully"
        }
    else:
        return {
            "success": False,
            "message": "MAC verification failed"
        } 

'''


# load persisted data on startup (if present)
_load(CARDS_FILE, cards)
@app.get("/ping")
def ping():
    return {"msg": "pong"}

@app.get('/check')
def check_trip(trip_id: str, controllor_id: str):
    


    #not yet implemented: checking copied cards which are scanned by the same controllor_id
    if trip_id in cards:
        return {"found": True, "details": cards[trip_id]}
    else:
        return {"found": False}


@app.post('/generate_trip')
def generate_trip(origin: str, destination: str, trip_type: str, timestamp: str):
    id_str = str(uuid.uuid4())
    cards[id_str] = {"origin": origin, "destination": destination, "timestamp": timestamp, "type": trip_type}
    _save(CARDS_FILE, cards)
    return {"id": id_str}




# @app.get('/cards')
# def list_trips():
#     return {"cards": sorted(list(cards))}


if __name__ == "__main__":
    # Start the ASGI server when running `python app.py` directly
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)