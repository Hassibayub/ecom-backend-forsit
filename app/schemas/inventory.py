from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .base import TimestampMixin, BaseResponse

class InventoryBase(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=0)
    low_stock_threshold: int = Field(..., ge=0)

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    quantity: Optional[int] = Field(None, ge=0)
    low_stock_threshold: Optional[int] = Field(None, ge=0)

class InventoryResponse(InventoryBase, BaseResponse, TimestampMixin):
    class Config:
        from_attributes = True 