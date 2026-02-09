from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VaultTransactionBase(BaseModel):
    allocation_id: int
    type: str
    timestamp: datetime

class VaultTransactionCreate(BaseModel):
    allocation_id: int
    type: str

class VaultTransactionUpdate(BaseModel):
    type: Optional[str] = None

class VaultTransactionInDBBase(VaultTransactionBase):
    id: int

    class Config:
        from_attributes = True

class VaultTransaction(VaultTransactionInDBBase):
    pass
