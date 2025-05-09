from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


def get_project(db: Session, project_id: int) -> Optional[Project]:
    """
    Ottiene un progetto dal database tramite il suo ID.
    """
    return db.query(Project).filter(Project.id == project_id).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100) -> List[Project]:
    """
    Ottiene una lista di progetti con paginazione.
    """
    return db.query(Project).offset(skip).limit(limit).all()


def get_active_projects(db: Session, skip: int = 0, limit: int = 100) -> List[Project]:
    """
    Ottiene i progetti attivi.
    """
    return db.query(Project).filter(Project.is_active == True).offset(skip).limit(limit).all()


def create_project(db: Session, project: ProjectCreate) -> Project:
    """
    Crea un nuovo progetto nel database.
    """
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, project_id: int, project: ProjectUpdate) -> Optional[Project]:
    """
    Aggiorna un progetto esistente.
    """
    db_project = get_project(db, project_id)
    if not db_project:
        return None

    # Aggiorna solo i campi presenti nell'update
    update_data = project.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)

    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int) -> bool:
    """
    Elimina un progetto dal database.
    """
    db_project = get_project(db, project_id)
    if not db_project:
        return False

    db.delete(db_project)
    db.commit()
    return True
