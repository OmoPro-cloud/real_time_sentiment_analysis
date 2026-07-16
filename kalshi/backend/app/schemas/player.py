from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

class PlayerBase(BaseModel):
    full_name: str
    known_as: str | None = None
    date_of_birth: date
    nationality: str

    club_id: int | None = None
    national_team_id: int | None = None

    primary_position: str
    secondary_position: str | None = None
    preferred_foot: str | None = None

    height_cm: int | None = None
    weight_kg: int | None = None
    shirt_number: int | None = None

    market_value: int | None = None
    contract_until: date | None = None
    agent: str | None = None

    is_active: bool = True

class PlayerCreate(PlayerBase):
    pass

class PlayerResponse(PlayerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)