from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.tournament import Tournament
from app.schemas.tournament import (
    TournamentCreate,
    TournamentResponse,
)

router = APIRouter(
    prefix="/tournaments",
    tags=["Tournaments"],
)


@router.post(
    "",
    response_model=TournamentResponse,
)
def create_tournament(
    tournament: TournamentCreate,
    db: Session = Depends(get_db),
):

    db_tournament = Tournament(
        name=tournament.name,
        code=tournament.code,
        country=tournament.country,
        confederation=tournament.confederation,
        tournament_type=tournament.tournament_type,
        founded_year=tournament.founded_year,
        current_champion=tournament.current_champion,
        most_titles_club=tournament.most_titles_club,
        most_titles_count=tournament.most_titles_count,
    )

    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)

    return db_tournament


@router.get(
    "",
    response_model=list[TournamentResponse],
)
def get_tournaments(
    db: Session = Depends(get_db),
):
    return db.query(Tournament).all()