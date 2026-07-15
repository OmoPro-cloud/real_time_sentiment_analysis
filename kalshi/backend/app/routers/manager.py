from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.manager import Manager
from app.schemas.manager import (
    ManagerCreate,
    ManagerResponse,
)

router = APIRouter(
    prefix="/managers",
    tags=["Managers"],
)

@router.post(
    "",
    response_model=ManagerResponse,
)
def create_manager(
    manager: ManagerCreate,
    db: Session = Depends(get_db),
):
    db_manager = Manager(
        full_name=manager.full_name,
        nationality=manager.nationality,
        current_team=manager.current_team,
        preferred_formation=manager.preferred_formation,
        secondary_formation=manager.secondary_formation,
        tactical_style=manager.tactical_style,
        coaching_since=manager.coaching_since,
        date_of_birth=manager.date_of_birth,
    )

    db.add(db_manager)
    db.commit()
    db.refresh(db_manager)

    return db_manager

@router.get(
    "",
    response_model=list[ManagerResponse],
)
def get_managers(
    db: Session = Depends(get_db),
): return db.query(Manager).all()