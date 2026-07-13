from fastapi import FastAPI

from app.database import Base, engine
from app import models

#Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return{"message": "Welcome to the Kalshi Ai Dashboard!"}

@app.get("/matches")
def matches():
    return{"message": "Today's Matches: Match 1, Match2, Match 3"}