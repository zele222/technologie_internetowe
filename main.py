from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from models import Person, PersonCreate, PersonNameUpdate, PositionUpdate
from db_config import ORMBaseModel, db_engine, get_db_session
from encoders import to_dict
from typing import List
import os
import json
from shapely import wkt

app = FastAPI()

# CORS (opcjonalnie)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL")

active_connections: list[WebSocket] = []


ORMBaseModel.metadata.create_all(bind=db_engine)



@app.get("/")
def test():
    return {"Hello": "World"}


@app.post("/people")
def create_person(person_create: PersonCreate, db_session: Session=Depends(get_db_session)):
    new_person = Person(
        first_name = person_create.first_name,
        last_name = person_create.last_name,
        person_type_id = person_create.person_type_id
    )
    
    db_session.add(new_person)
    db_session.commit()
    db_session.refresh(new_person)
    return jsonable_encoder({
        "id": new_person.id,
        "first_name":new_person.first_name,
        "last_name":new_person.last_name,
        "person_type_id":person_create.person_type_id
    })


@app.get("/people")
def get_all_people(db_session: Session = Depends(get_db_session)):
    people = db_session.query(Person).all()
    result = []
    for person in people:
        person_dict = to_dict(person)
        result.append(person_dict)
    return jsonable_encoder(result)

@app.put("/people/{person_id}/name")
def update_names(person_id: int, names_update: PersonNameUpdate, db_session: Session = Depends(get_db_session)):
    person = db_session.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404,detail="Person not found")
    person.first_name = f"first_name:{names_update.first_name}"
    person.last_name = f"last_name:{names_update.last_name}"
    db_session.commit()
    db_session.refresh(person)
    return jsonable_encoder({
        "message": "Names updated",
        "id": person.id,
        "first_name": names_update.first_name,
        "last_name": names_update.last_name
    })

@app.delete("/people/{person_id}")
def delete_user(person_id: int, db_session: Session = Depends(get_db_session)):
    person = db_session.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404,detail="Person not found")
    db_session.delete(person)
    db_session.commit()
    return jsonable_encoder({"message" : "Person deleted"})

@app.websocket("/ws/positions")
async def positions(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Utrzymanie połączenia
    except WebSocketDisconnect:
        active_connections.remove(websocket)

@app.put("/people/{person_id}/position")
async def update_position(person_id: int, position_update: PositionUpdate, db_session: Session = Depends(get_db_session)):
    from geoalchemy2.shape import to_shape
    from shapely import wkt
    import json

    person = db_session.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    # Przypisanie nowej pozycji w formacie WKT
    geom = wkt.loads(position_update.position)
    person.position = position_update.position
    person.latitude = geom.y
    person.longitude = geom.x
    db_session.commit()
    db_session.refresh(person)

    # Wiadomość do klientów WebSocket
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

    return {"message": "Position updated"}
