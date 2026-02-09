from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from app.db.base import Base

class Vault(Base):
    __tablename__ = "vaults"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=False)
    total_lockers = Column(Integer, nullable=False)
    available_lockers = Column(Integer, nullable=False)
    status = Column(Enum("OPERATIONAL", "MAINTENANCE", "CLOSED", name="vault_status"), nullable=False)

    lockers = relationship("Locker", back_populates="vault")
