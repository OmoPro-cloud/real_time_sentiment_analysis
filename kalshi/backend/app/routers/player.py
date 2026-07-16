from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.club import Club
from app.models.national_team import NationalTeam
from app.models.player import Player
from app.schemas.player import PlayerCreate, PlayerResponse

router = APIRouter(
    prefix="/players",
    tags=["Players"],
)

@router.post(
    "",
    response_model=PlayerResponse,
    status_code=201,
)
def CreatePlayer(
    player: PlayerCreate,
    db: Session = Depends(get_db),
):
    #Validate the supplied club ID
    if player.club_id is not None:
        db_club = (
            db.query(Club)
            .filter(Club.id == player.club_id)
            .first()
        )

        if db_club is None:
            raise HTTPException(
                status_code=404,
                detail="Club not found",
            )
        
    #Validate the supplied National Team ID
    if player.national_team_id is not None:
        db_national_team = (
            db.query(NationalTeam)
            .filter(
                NationalTeam.id == player.national_team_id
            )
            .first()
        )

        if db_national_team is None:
            raise HTTPException(
                status_code=404,
                detail="National team not found",
            )

    db_player = Player(
        full_name=player.full_name,
        known_as=player.known_as,
        date_of_birth=player.date_of_birth,
        nationality=player.nationality,
        club_id=player.club_id,
        national_team_id=player.national_team_id,
        primary_position=player.primary_position,
        secondary_position=player.secondary_position,
        preferred_foot=player.preferred_foot,
        height_cm=player.height_cm,
        weight_kg=player.weight_kg,
        shirt_number=player.shirt_number,
        market_value=player.market_value,
        contract_until=player.contract_until,
        agent=player.agent,
        is_active=player.is_active,
        )
    
    try:
        db.add(db_player)
        db.commit()
        db.refresh(db_player)

    except IntegrityError as exc:
        db.rollback()

        print("PLAYER INSERT ERROR:", exc.orig)

        raise HTTPException(
            status_code=400,
            detail="Player could not be added because of invalid or conflicting data"
        )
    
    return db_player

@router.get(
    "",
    response_model=list[PlayerResponse],
)
def get_players(
    db: Session = Depends(get_db),
):
    return (
        db.query(Player)
        .order_by(Player.id)
        .all()
    )

@router.get(
    "/{player_id}",
    response_model=PlayerResponse,
)
def get_player(
    player_id: int,
    db: Session = Depends(get_db),
):
    db_player = (
        db.query(Player)
        .filter(Player.id == player_id)
        .first()
    )

    if db_player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )
    return db_player