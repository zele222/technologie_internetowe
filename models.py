from sqlalchemy import Column, Integer, String
from db_config import ORMBaseModel
from pydantic import BaseModel
from geoalchemy2 import Geometry

# TODO Wzorując się na poniższych przykładach, zdefiniuj odpowienie modele w swojej aplikacji.

from sqlalchemy import Column, Integer, String, Float

class Person(ORMBaseModel):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    person_type_id = Column(Integer, index=True, nullable=False)
    position = Column(Geometry(geometry_type='POINT', srid=2180))
    latitude = Column(Float)
    longitude = Column(Float)

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

class PositionUpdate(BaseModel):
    position: str  # format WKT

