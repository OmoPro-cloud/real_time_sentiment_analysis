from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, model_validator

class SeasonBase(BaseModel):
    name: str
    start_date: date
    end_date: date
    is_current: bool = False

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date <= self.start_date:
            raise ValueError(
                "end_date must be later than start_date"
            )
        
        return self
    
class SeasonCreate(SeasonBase):
    pass 

class SeasonResponse(SeasonBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )