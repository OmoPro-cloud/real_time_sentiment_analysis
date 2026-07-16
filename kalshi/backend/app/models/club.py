from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    BigInteger,
    Integer,
    String,
)

from sqlalchemy import func
from app.database import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    club_code = Column(String(3), unique=True, nullable=False)

    country = Column(String, nullable=False)

    tournament_id = Column(
    Integer,
    ForeignKey("tournaments.id"),
    nullable=False,
    )

    city = Column(String)

    stadium = Column(String)

    founded_year = Column(Integer)

    club_value = Column(BigInteger)

    owner = Column(String)

    president = Column(String)

    is_active = Column(Boolean, default=True)

    tournament = relationship(
        "Tournament",
        back_populates="clubs",
    )

    managers = relationship(
        "Manager",
        back_populates="club",
    )

    players = relationship(
        "Player",
        back_populates="club",
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