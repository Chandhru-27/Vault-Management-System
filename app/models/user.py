from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum("CUSTOMER", "STAFF", "ADMIN", name="user_role"), nullable=False)
    status = Column(Enum("ACTIVE", "INACTIVE", "SUSPENDED", name="user_status"), nullable=False)

    allocations = relationship("LockerAllocation", back_populates="user")
