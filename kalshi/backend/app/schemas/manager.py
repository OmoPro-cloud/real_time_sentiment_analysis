from pydantic import BaseModel

class ManagerCreate(BaseModel): #what the api will ask for
    full_name: str
    nationality: str

    club_id: int | None = None

    preferred_formation: str | None = None
    secondary_formation: str | None = None

    tactical_style: str | None = None

    coaching_since: int | None = None

    date_of_birth: str | None = None

    is_active: bool = True

    preferred_foot: str | None = None
    contract_until: str | None = None
    annual_salary: int | None = None
    agent: str | None = None
    playing_position: str | None = None

class ManagerResponse(BaseModel): #what the api will display when called by the user
    id: int

    full_name: str
    nationality: str

    club_id: int | None = None

    preferred_formation: str | None = None
    secondary_formation: str | None = None

    tactical_style: str | None = None

    coaching_since: int | None = None

    date_of_birth: str | None = None

    is_active: bool

    preferred_foot: str | None = None
    contract_until: str | None = None
    annual_salary: int | None = None
    agent: str | None = None
    playing_position: str | None = None

    class Config:
        from_attributes = True