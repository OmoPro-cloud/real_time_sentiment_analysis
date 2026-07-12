from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return{"message": "Welcome to the Kalshi Ai Dashboard!"}

@app.get("/matches")
def matches():
    return{"message": "Today's Matches: Match 1, Match2, Match 3"}