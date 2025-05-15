from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .base import TimestampMixin, BaseResponse

class SaleBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    amount: float = Field(..., gt=0)
    sale_date: datetime

class SaleCreate(SaleBase):
    pass

class SaleUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0)
    amount: Optional[float] = Field(None, gt=0)
    sale_date: Optional[datetime] = None

class SaleResponse(SaleBase, BaseResponse, TimestampMixin):
    id: int

    class Config:
        from_attributes = True

class RevenueResponse(BaseModel):
    interval: str
    revenue: float
    total_sales: int 