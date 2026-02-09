from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role: str = "CUSTOMER"
    status: str = "ACTIVE"

class UserUpdate(UserBase):
    password: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    role: str
    status: str

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str
