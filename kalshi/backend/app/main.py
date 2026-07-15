from fastapi import FastAPI

from app.database import Base, engine
from app.models import(
    NationalTeam,
    Manager,
    Club,
    Tournament,
)

from app.routers import (
    national_team,
    manager,
    club,
    tournament,
)

app = FastAPI()

app.include_router(national_team.router)
app.include_router(manager.router)
app.include_router(club.router)
app.include_router(tournament.router)

@app.get("/")
def home():
    return {"message": "Welcome to the Kalshi AI Dashboard!"}

@app.get("/matches")
def matches():
    return{"message": "Today's Matches: Match 1, Match2, Match 3"}