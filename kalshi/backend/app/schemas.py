from pydantic import BaseModel


class TeamCreate(BaseModel): #this basically says: "this is what I need from the user"
    name: str
    fifa_code: str
    fifa_rank: int
    elo_rating: float
    confederation: str

class TeamResponse(BaseModel): #this is what the API returns
    id: int
    name: str
    fifa_code: str
    fifa_rank: int
    elo_rating: float
    confederation: str

    class Config:
        from_attributes = True