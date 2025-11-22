from fastapi import FastAPI
import uuid
app = FastAPI()

cards = set()

@app.get("/ping")
def ping():
    return {"msg": "pong"}

@app.get('/generate_card')
def generate_card():
    id = uuid.UUID()
    cards.add(id)
    return id