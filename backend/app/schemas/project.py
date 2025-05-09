from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Schema base per i progetti


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[str] = None
    is_active: bool = True

# Schema per la creazione di un progetto


class ProjectCreate(ProjectBase):
    pass

# Schema per l'aggiornamento di un progetto (tutti i campi sono opzionali)


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None

# Schema per l'output di un progetto (include i campi di database)


class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
