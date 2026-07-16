from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy import func

from app.database import Base


class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    code = Column(String(5), unique=True, nullable=False)

    country = Column(String, nullable=False)

    confederation = Column(String)

    tournament_type = Column(String)

    founded_year = Column(String)

    current_champion = Column(String)

    most_titles_club = Column(String)

    most_titles_count = Column(Integer)

    clubs = relationship(
        "Club",
        back_populates="tournament",
    )

    competition_seasons = relationship(
        "CompetitionSeason",
        back_populates="tournament",
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )