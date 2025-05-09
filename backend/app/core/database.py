from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import os

# Creazione engine per la connessione al database
engine = create_engine(settings.DATABASE_URL)

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
