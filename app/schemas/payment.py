from pydantic import BaseModel, Field
from typing import Optional

class PaymentBase(BaseModel):
    allocation_id: int
    amount: float
    status: str

class PaymentCreate(BaseModel):
    allocation_id: int
    # BUG: Easy bug - Allows negative amounts for payments.
    amount: float = Field(..., gt=-1)
    status: str = "PENDING"

class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    status: Optional[str] = None

class PaymentInDBBase(PaymentBase):
    id: int

    class Config:
        from_attributes = True

class Payment(PaymentInDBBase):
    pass
