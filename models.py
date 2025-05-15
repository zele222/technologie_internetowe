from sqlalchemy import Column, Integer, String
from db_config import ORMBaseModel
from pydantic import BaseModel

# TODO Wzorując się na poniższych przykładach, zdefiniuj odpowienie modele w swojej aplikacji.

class Person(ORMBaseModel):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    person_type_id = Column(Integer, index=True, nullable=False)

class PersonCreate(BaseModel):
    first_name: str
    last_name: str
    person_type_id: int
#    position: str  # format WKT, np. "POINT(123 456)"

#class PositionUpdate(BaseModel):
#    position: str  # format WKT

class PersonNameUpdate(BaseModel):
    first_name: str
    last_name: str

