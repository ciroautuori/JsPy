from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
import os
import shutil
import uuid

from app.core.database import get_db
from app.core.config import settings
from app.schemas.project import Project as ProjectSchema, ProjectCreate, ProjectUpdate
from app.crud import project as project_crud

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=List[ProjectSchema])
def read_projects(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
    db: Session = Depends(get_db)
):
    """
    Ottenere l'elenco dei progetti, con opzione per filtrare solo quelli attivi.
    """
    if active_only:
        projects = project_crud.get_active_projects(db, skip=skip, limit=limit)
    else:
        projects = project_crud.get_projects(db, skip=skip, limit=limit)
    return projects


@router.get("/{project_id}", response_model=ProjectSchema)
def read_project(project_id: int, db: Session = Depends(get_db)):
    """
    Ottenere un progetto specifico tramite il suo ID.
    """
    db_project = project_crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Progetto non trovato")
    return db_project


@router.post("/", response_model=ProjectSchema, status_code=status.HTTP_201_CREATED)
async def create_project(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    status: Optional[str] = Form(None),
    is_active: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Creare un nuovo progetto con possibilità di caricare un'immagine image.
    """
    # Gestione del caricamento dell'immagine
    image_url = None
    if image:
        # Crea directory se non esiste
        upload_dir = os.path.join(
            settings.STATIC_FILES_DIR, "images", "projects")
        os.makedirs(upload_dir, exist_ok=True)

        # Genera nome file univoco
        file_extension = os.path.splitext(image.filename)[1]
        file_name = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(upload_dir, file_name)

        # Salva il file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # URL relativo per accedere all'immagine
        image_url = f"/static/images/projects/{file_name}"

    # Crea oggetto progetto
    project_data = ProjectCreate(
        name=name,
        description=description,
        status=status,
        image_url=image_url,
        is_active=is_active
    )

    return project_crud.create_project(db=db, project=project_data)


@router.put("/{project_id}", response_model=ProjectSchema)
async def update_project(
    project_id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    status: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Aggiornare un progetto esistente.
    """
    # Verifica che il progetto esista
    db_project = project_crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Progetto non trovato")

    # Gestione del caricamento della nuova immagine, se presente
    image_url = None
    if image:
        # Crea directory se non esiste
        upload_dir = os.path.join(
            settings.STATIC_FILES_DIR, "images", "projects")
        os.makedirs(upload_dir, exist_ok=True)

        # Elimina la vecchia immagine se esiste
        if db_project.image_url:
            old_image_path = os.path.join(
                settings.STATIC_FILES_DIR, db_project.image_url.lstrip('/static/'))
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

        # Genera nome file univoco
        file_extension = os.path.splitext(image.filename)[1]
        file_name = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(upload_dir, file_name)

        # Salva il file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # URL relativo per accedere all'immagine
        image_url = f"/static/images/projects/{file_name}"

    # Crea oggetto per l'aggiornamento
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if description is not None:
        update_data["description"] = description
    if status is not None:
        update_data["status"] = status
    if is_active is not None:
        update_data["is_active"] = is_active
    if image_url is not None:
        update_data["image_url"] = image_url

    project_update = ProjectUpdate(**update_data)
    return project_crud.update_project(db=db, project_id=project_id, project=project_update)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """
    Eliminare un progetto.
    """
    # Verifica che il progetto esista
    db_project = project_crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Progetto non trovato")

    # Elimina l'immagine associata se esiste
    if db_project.image_url:
        image_path = os.path.join(
            settings.STATIC_FILES_DIR, db_project.image_url.lstrip('/static/'))
        if os.path.exists(image_path):
            os.remove(image_path)

    success = project_crud.delete_project(db=db, project_id=project_id)
    if not success:
        raise HTTPException(
            status_code=500, detail="Errore durante l'eliminazione")

    return None
