from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LockerAllocationBase(BaseModel):
    locker_id: int
    user_id: int
    allocated_at: datetime
    expiry_date: datetime
    status: str

class LockerAllocationCreate(BaseModel):
    locker_id: int
    user_id: int
    expiry_date: datetime

class LockerAllocationUpdate(BaseModel):
    expiry_date: Optional[datetime] = None
    status: Optional[str] = None

class LockerAllocationInDBBase(LockerAllocationBase):
    id: int

    class Config:
        from_attributes = True

class LockerAllocation(LockerAllocationInDBBase):
    pass
