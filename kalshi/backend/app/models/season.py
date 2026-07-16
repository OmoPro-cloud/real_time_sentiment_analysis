from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Integer,
    BigInteger,
    String,
    UniqueConstraint,
    func,
)

from app.database import Base

from sqlalchemy.orm import relationship

class Season(Base):
    __tablename__ = "seasons"

    __table_args__ = (
        UniqueConstraint(
            "name",
            name="unique_season_name",
        ),
    )

    id = Column(
        Integer, primary_key=True,
        index=True,
    )

    name = Column(
        String(9),
        nullable=False,
    )

    start_date = Column(
        Date,
        nullable=False,
    )

    end_date = Column(
        Date,
        nullable=False,
    )

    is_current = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false"
    )

    competition_seasons = relationship(
        "CompetitionSeason",
        back_populates="season",
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