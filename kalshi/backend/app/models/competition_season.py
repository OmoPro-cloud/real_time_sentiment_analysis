from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.database import Base

class CompetitionSeason(Base):
    __tablename__ = "competition_seasons"

    __table_args__ = (
        UniqueConstraint(
            "tournament_id",
            "season_id",
            name="unique_competition_season",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    tournament_id = Column(
        Integer,
        ForeignKey("tournaments.id"),
        nullable=False,
    )

    season_id = Column(
        Integer,
        ForeignKey("seasons.id"),
        nullable=True,
    )

    start_date = Column(
        Date,
        nullable=True,
    )

    end_date = Column(
        Date,
        nullable=True,
    )

    status = Column(
        String,
        nullable=False,
        default="scheduled",
        server_default="scheduled",
    )

    current_matchweek = Column(
        Integer,
        nullable=True,
    )

    winner_club_id = Column(
        Integer,
        ForeignKey("clubs.id"),
        nullable=True,
    )

    tournament = relationship(
        "Tournament",
        back_populates="competition_seasons"
    )

    season = relationship(
        "Season",
        back_populates="competition_seasons",
    )

    winner_club = relationship(
        "Club",
        foreign_keys=[winner_club_id],
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )