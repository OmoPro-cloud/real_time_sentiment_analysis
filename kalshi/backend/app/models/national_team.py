from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.database import Base

from sqlalchemy.orm import relationship


class NationalTeam(Base):
    __tablename__ = "national_teams"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    fifa_code = Column(String(3), unique=True, nullable=False)

    country = Column(String, nullable=False)
    confederation = Column(String, nullable=False)

    association_name = Column(String, nullable=True)
    nickname = Column(String, nullable=True)
    home_stadium = Column(String, nullable=True)
    headquarters_city = Column(String, nullable=True)
    founded_year = Column(Integer, nullable=True)

    is_active = Column(Boolean, default=True)

    players = relationship(
        "Player",
        back_populates="national_team",
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