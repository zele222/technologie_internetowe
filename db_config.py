from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#zainstaluj postgres zmien ten database url w zmiennych srodowiskowych zeby byly nazwai haslo


#DATABASE_URL = "postgresql://postgres:<db_password>@localhost:5432/indoor_cod.db" # TODO
#DATABASE_URL = "sqlite:///./indoor_cod.db"
#db_engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

DATABASE_URL = os.getenv("DATABASE_URL")
db_engine = create_engine(DATABASE_URL)

DBSession = sessionmaker(
    bind=db_engine, 
    autocommit=False, 
    autoflush=False
)
ORMBaseModel = declarative_base()

def get_db_session():
    db_session = DBSession()
    try:
        yield db_session 
    finally:
        db_session.close()
