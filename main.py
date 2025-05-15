from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from models import Person, PersonCreate, PersonNameUpdate
from db_config import ORMBaseModel, db_engine, get_db_session
from encoders import to_dict
from typing import Union

import os

DATABASE_URL = os.getenv("DATABASE_URL")

ORMBaseModel.metadata.create_all(bind=db_engine)
app = FastAPI()


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
