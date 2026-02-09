from sqlalchemy import Column, Integer, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime

from app.db.base import Base

class VaultTransaction(Base):
    __tablename__ = "vault_transactions"

    id = Column(Integer, primary_key=True, index=True)
    allocation_id = Column(Integer, ForeignKey("locker_allocations.id"), nullable=False)
    type = Column(Enum("DEPOSIT", "WITHDRAW", name="transaction_type"), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    allocation = relationship("LockerAllocation", back_populates="transactions")
