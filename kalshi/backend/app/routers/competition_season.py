from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.club import Club
from app.models.competition_season import CompetitionSeason
from app.models.season import Season
from app.models.tournament import Tournament
from app.schemas.competition_season import (
    CompetitionSeasonCreate,
    CompetitionSeasonResponse,
)

router = APIRouter(
    prefix="/competition-seasons",
    tags=["Competition Seasons"],
)

@router.post(
    "",
    response_model=CompetitionSeasonResponse,
    status_code=201,
)
def create_competition_season(
    competition_season: CompetitionSeasonCreate,
    db: Session = Depends(get_db),
):
    tournament = (
        db.query(Tournament)
        .filter(
            Tournament.id == competition_season.tournament_id
        )
        .first()
    )

    if tournament is None:
        raise HTTPException(
            status_code=404,
            detail="Tournament not found",
        )
    
    season = (
        db.query(Season)
        .filter(
            Season.id == competition_season.season_id
        )
        .first()
    )

    if season is None:
        raise HTTPException(
            status_code=4040,
            detail="Season not found"
        )
    
    if competition_season.winner_club_id is not None:
        winner_club = (
            db.query(Club)
            .filter(
                Club.id == competition_season.winner_club_id
            )
            .first()
        )

        if winner_club is None:
            raise HTTPException(
                status_code=404,
                detail="Winner club not found",
            )
        
    db_competition_season = CompetitionSeason(
        tournament_id=competition_season.tournament_id,
        season_id=competition_season.season_id,
        start_date=competition_season.start_date,
        end_date=competition_season.end_date,
        status=competition_season.status,
        current_matchweek=competition_season.current_matchweek,
        number_of_clubs=competition_season.number_of_clubs,
        winner_club_id=competition_season.winner_club_id,
    )

    try:
        db.add(db_competition_season)
        db.commit()
        db.refresh(db_competition_season)

    except IntegrityError as exc:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="This tournament season already exists",
        ) from exc
    
    return db_competition_season

@router.get(
    "",
    response_model=list[CompetitionSeasonResponse],
)
def get_competition_seasons(
    db: Session = Depends(get_db),
):
    return (
        db.query(CompetitionSeason)
        .order_by(CompetitionSeason.id)
        .all()
    )

@router.get(
    "/{competition_season_id}",
    response_model=CompetitionSeasonResponse,
)
def get_competition_season(
    competition_season_id: int,
    db: Session = Depends(get_db),
):
    db_competition_season = (
        db.query(CompetitionSeason)
        .filter(
            CompetitionSeason.id == competition_season_id
        )
        .first()
    )

    if db_competition_season is None:
        raise HTTPException(
            status_code=404,
            detail="Competition season not found",
        )
    
    return db_competition_season