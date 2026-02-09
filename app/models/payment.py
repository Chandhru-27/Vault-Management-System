from sqlalchemy import Column, Integer, Enum, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.db.base import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    allocation_id = Column(Integer, ForeignKey("locker_allocations.id"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum("SUCCESSFUL", "FAILED", "PENDING", name="payment_status"), nullable=False)

    allocation = relationship("LockerAllocation", back_populates="payments")
