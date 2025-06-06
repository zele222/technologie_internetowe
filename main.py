import os
import json
from fastapi import FastAPI, APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from models import Person, PersonCreate, PositionUpdate
from db_config import get_db_session, ORMBaseModel, db_engine
from encoders import to_dict
from fastapi.middleware.cors import CORSMiddleware  # <-- Dodaj to


# Tworzenie tabel przy starcie
ORMBaseModel.metadata.create_all(bind=db_engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- zezwala na wszystkie domeny
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
router = APIRouter()

# Lista aktywnych WebSocketów
active_connections: list[WebSocket] = []

@router.post("/person/")
def create_person(person: PersonCreate, db: Session = Depends(get_db_session)):
    db_person = Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return to_dict(db_person)

@router.get("/person/")
def read_all_persons(db: Session = Depends(get_db_session)):
    persons = db.query(Person).all()
    return [to_dict(p) for p in persons]

@router.get("/person/{person_id}")
def read_person(person_id: int, db: Session = Depends(get_db_session)):
    person = db.query(Person).filter(Person.id == person_id).first()
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return to_dict(person)

@router.put("/person/{person_id}")
def update_person(person_id: int, updated: PersonCreate, db: Session = Depends(get_db_session)):
    person = db.query(Person).filter(Person.id == person_id).first()
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    for key, value in updated.dict().items():
        setattr(person, key, value)
    db.commit()
    return to_dict(person)

@router.delete("/person/{person_id}")
def delete_person(person_id: int, db: Session = Depends(get_db_session)):
    person = db.query(Person).filter(Person.id == person_id).first()
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    db.delete(person)
    db.commit()
    return {"message": f"Deleted person with ID {person_id}"}

# ➕ ENDPOINT DO AKTUALIZACJI POZYCJI
@app.put("/person/{person_id}/position")
async def update_position(person_id: int, position: PositionUpdate, db: Session = Depends(get_db_session)):
    person = db.query(Person).filter(Person.id == person_id).first()
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")

    person.latitude = position.latitude
    person.longitude = position.longitude
    db.commit()
    db.refresh(person)

    message = json.dumps({
        "id": person.id,
        "lat": person.latitude,
        "lon": person.longitude,
        "first_name": person.first_name,
        "last_name": person.last_name,
        "person_type_id": person.person_type_id
    })

    for connection in active_connections:
        await connection.send_text(message)

    return {"status": "position updated"}

# 🌐 WEBSOCKET /ws/positions
@app.websocket("/ws/positions")
async def websocket_positions(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # tylko utrzymuje połączenie
    except WebSocketDisconnect:
        active_connections.remove(websocket)

# Rejestracja routera
app.include_router(router)
