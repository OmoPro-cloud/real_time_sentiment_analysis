from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.national_team import NationalTeam
from app.schemas.national_team import (
    NationalTeamCreate,
    NationalTeamResponse,
)

router = APIRouter(
    prefix="/national-teams",
    tags=["National Teams"],
)

@router.post(
    "",
    response_model=NationalTeamResponse,
)
def create_national_team(
    team: NationalTeamCreate,
    db: Session = Depends(get_db),
):
    db_team = NationalTeam(
        name=team.name,
        fifa_code=team.fifa_code,
        country=team.country,
        confederation=team.confederation,
        association_name=team.association_name,
        nickname=team.nickname,
        home_stadium=team.home_stadium,
        headquarters_city=team.headquarters_city,
        founded_year=team.founded_year,
    )

    db.add(db_team)
    db.commit()
    db.refresh(db_team)

    return db_team

@router.get(
    "",
    response_model=list[NationalTeamResponse],
)
def get_national_teams(
    db: Session = Depends(get_db),
):
    return db.query(NationalTeam).all()