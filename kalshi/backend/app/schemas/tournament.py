from pydantic import BaseModel


class TournamentCreate(BaseModel):

    name: str

    code: str

    country: str

    confederation: str | None = None

    tournament_type: str | None = None

    founded_year: str | None = None

    current_champion: str | None = None

    most_titles_club: str | None = None

    most_titles_count: int | None = None


class TournamentResponse(BaseModel):

    id: int

    name: str

    code: str

    country: str

    confederation: str | None = None

    tournament_type: str | None = None

    founded_year: str | None = None

    current_champion: str | None = None

    most_titles_club: str |None = None

    most_titles_count: int | None = None

    class Config:
        from_attributes = True