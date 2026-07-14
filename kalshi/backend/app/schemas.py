from pydantic import BaseModel


class NationalTeamCreate(BaseModel):
    name: str
    fifa_code: str
    confederation: str
    association_name: str

    nickname: str | None = None
    home_stadium: str | None = None
    headquarters_city: str | None = None
    founded_year: int | None = None

class NationalTeamResponse(BaseModel):
    id: int

    name: str
    fifa_code: str

    country: str
    confederation: str
    association_name: str

    nickname: str | None = None
    home_stadium: str | None = None
    headquarters_city: str | None = None
    founded_year: int | None = None

    class Config:
        from_attributes = True