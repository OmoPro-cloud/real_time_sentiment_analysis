from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.manager import Manager
from app.schemas.manager import (
    ManagerCreate,
    ManagerResponse,
)

from fastapi import HTTPException
from app.models.club import Club

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
    if manager.club_id is not None:

        db_club = (
            db.query(Club)
            .filter(Club.id == manager.club_id)
            .first()
        )

        if db_club is None:
            raise HTTPException(
                status_code=404,
                detail="Club not found"
            )
        
    db_manager = Manager(
        full_name=manager.full_name,
        nationality=manager.nationality,
        club_id=manager.club_id,
        preferred_formation=manager.preferred_formation,
        secondary_formation=manager.secondary_formation,
        tactical_style=manager.tactical_style,
        coaching_since=manager.coaching_since,
        date_of_birth=manager.date_of_birth,
        is_active=manager.is_active,
        preferred_foot=manager.preferred_foot,
        contract_until=manager.contract_until,
        annual_salary=manager.annual_salary,
        agent=manager.agent,
        playing_position=manager.playing_position,
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