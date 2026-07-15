from pydantic import BaseModel

class ManagerCreate(BaseModel): #what the api will ask for
    full_name: str
    nationality: str

    current_team: str | None = None

    preffered_formation: str | None = None
    secondary_formation: str | None = None

    tactical_style: str | None = None

    coaching_since: str | None = None

    date_of_birth: str | None = None

    is_active: bool = True

class ManagerResponse(BaseModel): #what the api will display when called by the user
    id: int

    full_name: str
    nationality: str

    current_team: str | None = None

    preferred_formation: str | None = None
    secondary_formation: str | None = None

    tactical_style: str | None = None

    coaching_since: str | None = None

    date_of_birth: str | None = None

    is_active: bool

    class Config:
        from_attributes = True