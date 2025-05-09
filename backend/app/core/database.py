from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


# Carica variabili d'ambiente da.env
config = load_dotenv()


# Ottenimento URL di connessione al database da.env
DATABASE_URL = os.getenv("DATABASE_URL")


# Creazione engine per la connessione al database
engine = create_engine(DATABASE_URL, connect_args={
                       "check_same_thread": False} if "sqlite" in DATABASE_URL else {})

# Definizione della sessione locale per la gestione delle transazioni
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Definizione della base della ORM per la gestione delle entità
Base = declarative_base()


# Funzione per ottenere una sessione locale per la gestione delle transazioni
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
