from sqlalchemy import Column, Integer, Enum, ForeignKey, DateTime
import datetime

from app.db.base import Base

class AccessLog(Base):
    __tablename__ = "access_logs"

    id = Column(Integer, primary_key=True, index=True)
    locker_id = Column(Integer, ForeignKey("lockers.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    access_type = Column(Enum("DEPOSIT", "WITHDRAW", "INSPECTION", name="access_type"), nullable=False)
