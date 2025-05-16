from typing import Optional

from pydantic import BaseModel, Field

from .base import BaseResponse, TimestampMixin


class InventoryBase(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=0)
    low_stock_threshold: int = Field(..., ge=0)

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    quantity: Optional[int] = None
    low_stock_threshold: Optional[int] = None

class InventoryResponse(InventoryBase, BaseResponse, TimestampMixin):
    id: int 