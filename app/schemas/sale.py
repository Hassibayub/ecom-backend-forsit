from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .base import TimestampMixin, BaseResponse

class SaleBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    total_amount: float = Field(..., gt=0)
    sale_date: datetime

class SaleCreate(SaleBase):
    pass

class SaleUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0)
    unit_price: Optional[float] = Field(None, gt=0)
    total_amount: Optional[float] = Field(None, gt=0)
    sale_date: Optional[datetime] = None

class SaleResponse(SaleBase, BaseResponse, TimestampMixin):
    id: int

class RevenueResponse(BaseModel):
    interval: str
    revenue: float
    total_sales: int

class PeriodRevenue(BaseModel):
    start_date: datetime
    end_date: datetime
    revenue: float

class ComparisonResponse(BaseModel):
    current_period: PeriodRevenue
    previous_period: PeriodRevenue
    percentage_change: float 