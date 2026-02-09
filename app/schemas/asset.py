from pydantic import BaseModel
from typing import Optional

class AssetBase(BaseModel):
    allocation_id: int
    asset_name: str
    estimated_value: float
    type: str

class AssetCreate(AssetBase):
    pass

class AssetUpdate(AssetBase):
    asset_name: Optional[str] = None
    estimated_value: Optional[float] = None
    type: Optional[str] = None

class AssetInDBBase(AssetBase):
    id: int

    class Config:
        from_attributes = True

class Asset(AssetInDBBase):
    pass
