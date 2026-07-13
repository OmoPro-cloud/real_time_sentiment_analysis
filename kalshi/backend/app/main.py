from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app import models, schemas

#Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return{"message": "Welcome to the Kalshi Ai Dashboard!"}

@app.post("/teams", response_model=schemas.TeamResponse)
def create_team(
    team: schemas.TeamCreate,
    db: Session = Depends(get_db),
):
    db_team = models.Team(
        name=team.name,
        fifa_code=team.fifa_code,
        fifa_rank=team.fifa_rank,
        elo_rating=team.elo_rating,
        confederation=team.confederation,
    )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

@app.get("/teams", response_model=list[schemas.TeamResponse])
def get_teams(db: Session = Depends(get_db)):
    teams = db.query(models.Team).all()
    return teams

@app.get("/matches")
def matches():
    return{"message": "Today's Matches: Match 1, Match2, Match 3"}