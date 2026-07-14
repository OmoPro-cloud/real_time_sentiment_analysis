from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.database import Base

class NationalTeam(Base):
    __tablename__ = "national_teams"

    id = Column(Integer, primary_key=True, index=True)

    #identity
    name = Column(String, nullable=False)
    fifa_code = Column(String(3), unique=True, nullable=False)

    #Geography
    country = Column(String, nullable=False)
    confederation = Column(String)
    

    #Federation
    association_name = Column(String, nullable=False)
    #fifa_rank = Column(Integer)

    #Optional
    nickname = Column(String, nullable=True)
    home_stadium = Column(String, nullable=True)
    headquarters_city = Column(String, nullable=True)
    founded_year = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


'''

from sqlalchemy import Column, Float, Integer, String, Boolean, DateTime
from datetime import datetime

from app.database import Base #every table in the database will inherit from Base

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True) #primary key, gives every team a unique ID e.g. 1, 2, 3, 4, 5
    name = Column(String, nullable=False) #nullable=False means this field MUST have a value
    fifa_code = Column(String(3), unique=True, nullable=False) #unique=True prevents duplicates
    fifa_rank = Column(Integer)
    elo_rating = Column(Float)
    confederation = Column(String)
    #country = Column(String, nullable=False)
    #is_active = Column(Boolean, default=True)
    #created_at = Column(DateTime, default=datetime.utcnow)

'''