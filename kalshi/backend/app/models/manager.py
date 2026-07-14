from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy import func

from app.database import Base

class Manager(Base):
    __tablename__ = "managers"

    id = Column(String, primary_key=True, index=True)

    full_name = Column(String, nullable=False)

    nationality = Column(String, nullable=False)

    current_team = Column(String)

    preferred_formation = Column(String)

    secondary_formation = Column(String)

    tactical_style = Column(String)

    coaching_since = Column(Integer)

    date_of_birth = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )