from sqlalchemy import (
    Boolean,
    Integer,
    BigInteger,
    Column,
    String,
    Date,
    DateTime,
    ForeignKey,
)
from sqlalchemy import func
from app.database import Base

from sqlalchemy.orm import relationship

class Player(Base):
    __tablename__ = "players"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    full_name = Column(String, nullable=False)

    known_as = Column(String, nullable=True)

    date_of_birth = Column(Date, nullable=False)

    nationality = Column(String, nullable=False)

    club_id = Column(
        Integer,
        ForeignKey("clubs.id"),
        nullable=True,
    )

    national_team_id = Column(
        Integer,
        ForeignKey("national_teams.id"),
        nullable=True,
    )

    primary_position = Column(String(5), nullable=False)

    secondary_position = Column(String(5), nullable=True)

    preferred_foot = Column(String)

    height_cm = Column(Integer, nullable=True)

    weight_kg = Column(Integer, nullable=True)

    shirt_number = Column(Integer, nullable=True)

    market_value = Column(BigInteger, nullable=True)

    contract_until = Column(Date, nullable=True)

    agent = Column(String, nullable=True)

    is_active = Column(Boolean, nullable=False, default=True, server_default="true")

    club = relationship(
        "Club",
        back_populates="players",
    )

    national_team = relationship(
        "NationalTeam",
        back_populates="players",
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