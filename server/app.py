from fastapi import FastAPI
import uuid
import uvicorn
import json
import os
import hmac
import hashlib
import base64
import logging

logger = logging.getLogger("uvicorn.error")

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



from pydantic import BaseModel

class ValidationRequest(BaseModel):
    uid: str
    counter: int
    mac: str
    challenge: str

def compute_mac(secret: str, data: str) -> str:
    """Compute Base64 HMAC-SHA256 of `data` using `secret`.

    Returns the Base64-encoded string without line breaks (matches Android's
    `Base64.NO_WRAP`).
    """
    mac = hmac.new(secret.encode("utf-8"), data.encode("utf-8"), hashlib.sha256).digest()
    return base64.b64encode(mac).decode("utf-8")


def validate_counter_and_mac(uid, counter, mac, challenge):
    # Ensure card exists
    if uid not in cards:
        logger.warning("Validation failed: unknown uid=%s", uid)
        return False
    card = cards[uid]

    # Expect stored fields: "counter" (int) and "secret_key" (str)
    try:
        card_counter = int(card.get("counter"))
    except Exception:
        logger.warning("Validation failed: invalid stored counter for uid=%s", uid)
        return False

    secret = card.get("secret_key")
    if secret is None:
        logger.warning("Validation failed: missing secret_key for uid=%s", uid)
        return False

    # Build combined string the same way as on the card/client: uid + challenge + stateCounter
    combined = f"{uid}{challenge}{card_counter}"
    computed_mac = compute_mac(secret, combined)

    # Verify counter matches and MAC matches (use constant-time compare)
    mac_ok = hmac.compare_digest(computed_mac, mac)
    try:
        provided_counter = int(counter)
    except Exception:
        provided_counter = counter

    if card_counter == provided_counter and mac_ok:
        # increment stored counter and persist
        cards[uid]["counter"] = card_counter + 1
        _save(CARDS_FILE, cards)
        return True

    # Log specific failure reason (without exposing secrets)
    logger.warning(
        "Validation failed for uid=%s: stored_counter=%s, provided_counter=%s, mac_ok=%s, challenge=%s",
        uid,
        card_counter,
        provided_counter,
        mac_ok,
        challenge,
    )
    return False
@app.post("/validate")
def validate_card(data: ValidationRequest):
    # Example: validate timestamp
    import time
    now = int(time.time() * 1000)


    # TODO: Put your MAC verification logic here
    if validate_counter_and_mac(data.uid, data.counter, data.mac, data.challenge):
        if False:#abs(now - data.timestamp) > 36000000000:
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