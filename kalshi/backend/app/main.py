from fastapi import FastAPI

from app.database import Base, engine
from app.models import NationalTeam, Manager
from app.routers import national_team, manager

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(national_team.router)
app.include_router(manager.router)

@app.get("/")
def home():
    return {"message": "Welcome to the Kalshi AI Dashboard!"}

@app.get("/matches")
def matches():
    return{"message": "Today's Matches: Match 1, Match2, Match 3"}