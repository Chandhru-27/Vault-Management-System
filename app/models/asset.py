from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.db.base import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    allocation_id = Column(Integer, ForeignKey("locker_allocations.id"), nullable=False)
    asset_name = Column(String, nullable=False)
    estimated_value = Column(Float, nullable=False)
    type = Column(Enum("JEWELRY", "DOCUMENT", "OTHER", name="asset_type"), nullable=False)

    allocation = relationship("LockerAllocation", back_populates="assets")
