from pydantic import BaseModel

class ClubCreate(BaseModel):

    name: str

    country: str

    club_code: str

    tournament_id: int

    city: str | None = None

    stadium: str | None = None

    founded_year: int | None = None

    club_value: int | None = None

    owner: str | None = None

    president: str | None = None

    is_active: bool = True

class ClubResponse(BaseModel):

    id: int

    name: str

    club_code: str

    country: str

    tournament_id: int

    city: str | None = None

    stadium: str | None = None

    founded_year: int | None = None

    club_value: int | None = None

    owner: str | None = None
    
    president: str | None = None

    is_active: bool

    class Config:
        from_attributes = True