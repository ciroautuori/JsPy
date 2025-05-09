import os
from pydantic import BaseModel
from dotenv import load_dotenv

# Carica le variabili di ambiente dal file .env
load_dotenv()


class Settings(BaseModel):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # API settings
    API_PREFIX: str = os.getenv("API_PREFIX", "/api")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Static files
    STATIC_FILES_DIR: str = os.getenv("STATIC_FILES_DIR", "app/static")

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")


# Istanza delle impostazioni da usare in tutta l'app
settings = Settings()
