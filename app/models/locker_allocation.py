from sqlalchemy import Column, Integer, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime

from app.db.base import Base

class LockerAllocation(Base):
    __tablename__ = "locker_allocations"

    id = Column(Integer, primary_key=True, index=True)
    locker_id = Column(Integer, ForeignKey("lockers.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    allocated_at = Column(DateTime, default=datetime.datetime.utcnow)
    expiry_date = Column(DateTime, nullable=False)
    status = Column(Enum("ACTIVE", "EXPIRED", "TERMINATED", name="allocation_status"), nullable=False)

    locker = relationship("Locker", back_populates="allocations")
    user = relationship("User", back_populates="allocations")
    assets = relationship("Asset", back_populates="allocation")
    transactions = relationship("VaultTransaction", back_populates="allocation")
    payments = relationship("Payment", back_populates="allocation")
