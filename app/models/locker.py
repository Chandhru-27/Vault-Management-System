from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.db.base import Base

class Locker(Base):
    __tablename__ = "lockers"

    id = Column(Integer, primary_key=True, index=True)
    vault_id = Column(Integer, ForeignKey("vaults.id"), nullable=False)
    locker_number = Column(String, nullable=False)
    size = Column(Enum("SMALL", "MEDIUM", "LARGE", name="locker_size"), nullable=False)
    status = Column(Enum("AVAILABLE", "ALLOCATED", "MAINTENANCE", name="locker_status"), nullable=False)
    monthly_rent = Column(Float, nullable=False)

    vault = relationship("Vault", back_populates="lockers")
    allocations = relationship("LockerAllocation", back_populates="locker")
