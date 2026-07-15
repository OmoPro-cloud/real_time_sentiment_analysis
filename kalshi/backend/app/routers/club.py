from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.club import Club
from app.models.tournament import Tournament
from app.schemas.club import (
    ClubCreate,
    ClubResponse,
)

router = APIRouter(
    prefix="/clubs",
    tags=["Clubs"],
)

@router.post(
    "",

)
def create_club(
    club: ClubCreate,
    db: Session = Depends(get_db),
):
    #Verify tournament exists
    db_tournament = (
        db.query(Tournament)
        .filter(Tournament.id == club.tournament_id)
        .first()
    )

    if db_tournament is None:
        raise HTTPException(
            status_code=404,
            detail="Tournament not found",
        )
    db_club = Club(
        name=club.name,
        club_code=club.club_code,
        country=club.country,
        tournament_id=club.tournament_id,
        city=club.city,
        stadium=club.stadium,
        founded_year=club.founded_year,
        club_value=club.club_value,
        owner=club.owner,
        president=club.president,
        is_active=club.is_active,
    )

    db.add(db_club)
    db.commit()
    db.refresh(db_club)

    return db_club

@router.get(
    "",
    response_model=list[ClubResponse],
)
def get_clubs(
    db: Session = Depends(get_db),
):
    return db.query(Club).all()