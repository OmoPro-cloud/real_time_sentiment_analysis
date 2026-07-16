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

class Manager(Base):
    __tablename__ = "managers"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String, nullable=False)

    nationality = Column(String, nullable=False)

    club_id = Column(
        Integer,
        ForeignKey("clubs.id"),
        nullable=True,
    )

    club = relationship(
        "Club",
        back_populates="managers",
    )

    preferred_formation = Column(String)

    secondary_formation = Column(String)

    tactical_style = Column(String)

    coaching_since = Column(Integer)

    date_of_birth = Column(String)

    is_active = Column(Boolean, default=True)

    preferred_foot = Column(String)

    contract_until = Column(String)

    annual_salary = Column(BigInteger)

    agent = Column(String)

    playing_position = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )  