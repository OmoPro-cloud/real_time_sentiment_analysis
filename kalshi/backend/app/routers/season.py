from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.season import Season
from app.schemas.season import (
    SeasonCreate,
    SeasonResponse,
)

router = APIRouter(
    prefix="/seasons",
    tags=["Seasons"],
)

@router.post(
    "",
    response_model=SeasonResponse,
    status_code=201,
)
def create_season(
    season: SeasonCreate,
    db: Session = Depends(get_db)
):
    db_season = Season(
        name=season.name,
        start_date=season.start_date,
        end_date=season.end_date,
        is_current=season.is_current,
    )

    try:
        db.add(db_season)
        db.commit()
        db.refresh(db_season)

    except IntegrityError as exc:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="A season with this name already exists",
        ) from exc
    
    return db_season

@router.get(
    "",
    response_model=list[SeasonResponse],
)
def get_seasons(
    db: Session = Depends(get_db),
):
    return (
        db.query(Season)
        .order_by(Season.start_date.desc())
        .all()
    )

@router.get(
    "/{season_id}",
    response_model=SeasonResponse,
)
def get_season(
    season_id: int,
    db: Session = Depends(get_db),
):
    db_season = (
        db.query(Season)
        .filter(Season.id == season_id)
        .first()
    )

    if db_season is None:
        raise HTTPException(
            status_code=404,
            detail="Season not found",
        )
    
    return db_season