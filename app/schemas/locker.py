from pydantic import BaseModel
from typing import Optional

class LockerBase(BaseModel):
    vault_id: int
    locker_number: str
    size: str
    status: str
    monthly_rent: float

class LockerCreate(LockerBase):
    pass

class LockerUpdate(LockerBase):
    vault_id: Optional[int] = None
    locker_number: Optional[str] = None
    size: Optional[str] = None
    status: Optional[str] = None
    monthly_rent: Optional[float] = None

class LockerInDBBase(LockerBase):
    id: int

    class Config:
        from_attributes = True

class Locker(LockerInDBBase):
    pass
