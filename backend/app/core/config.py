import os
from pydantic import BaseModel
from dotenv import load_dotenv

# Carica le variabili di ambiente dal file .env
load_dotenv()


class Settings(BaseModel):
    API_PREFIX: str = os.getenv("API_PREFIX", "/api")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    STATIC_FILES_DIR: str = os.path.join(os.getcwd(), "static")


# Istanza delle impostazioni da usare in tutta l'app
settings = Settings()
