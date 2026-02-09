from pydantic import BaseModel
from typing import Optional

class VaultBase(BaseModel):
    location: str
    total_lockers: int
    available_lockers: int
    status: str

class VaultCreate(VaultBase):
    pass

class VaultUpdate(VaultBase):
    location: Optional[str] = None
    total_lockers: Optional[int] = None
    available_lockers: Optional[int] = None
    status: Optional[str] = None

class VaultInDBBase(VaultBase):
    id: int

    class Config:
        from_attributes = True

class Vault(VaultInDBBase):
    pass
