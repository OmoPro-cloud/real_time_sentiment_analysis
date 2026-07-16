from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, model_validator

class CompetitionSeasonBase(BaseModel):
    tournament_id: int
    season_id: int

    start_date: date | None = None
    end_date: date | None = None

    status: str = "scheduled"
    current_matchweek: int | None = None
    number_of_clubs: int | None = None
    winner_club_id: int | None = None

    @model_validator(mode="after")
    def validate_dates(self):
        if (
            self.start_date is not None
            and self.end_date is not None
            and self.end_date <= self.start_date
        ):
            raise ValueError(
                "end_date must be later that start_date"
            )
        
        return self
    
class CompetitionSeasonCreate(CompetitionSeasonBase):
    pass 

class CompetitionSeasonResponse(CompetitionSeasonBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )