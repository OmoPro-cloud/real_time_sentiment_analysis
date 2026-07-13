from sqlalchemy import Column, Float, Integer, String

from app.database import Base #every table in the database will inherit from Base

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True) #primary key, gives every team a unique ID e.g. 1, 2, 3, 4, 5
    name = Column(String, nullable=False) #nullable=False means this field MUST have a value
    fifa_code = Column(String(3), unique=True, nullable=False) #unique=True prevents duplicates
    fifa_rank = Column(Integer)
    elo_rating = Column(Float)
    confederation = Column(String)