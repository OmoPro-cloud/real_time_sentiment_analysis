from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from app.database import Base

class NationalTeam(Base):
    __tablename__ = "national_teams"

    id = Column(Integer, primary_key=True, index=True)

    #Identity
    name = Column(String, nullable=False)
    fifa_code = Column(String, nullable=False)

    #Geography
    country = Column(String, nullable=False)
    confederation = Column(String, nullable=False)

    #Federation
    association_name = Column(String, nullable=False)

    #Optional information
    nickname = Column(String, nullable=True)
    home_stadium = Column(String, nullable=True)
    headquarters_city = Column(String, nullable=True)
    founded_year = Column(Integer, nullable=True)

    #Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )