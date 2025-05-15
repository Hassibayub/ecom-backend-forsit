from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .base import TimestampMixin, BaseResponse

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    category_id: Optional[int] = None

class ProductResponse(ProductBase, BaseResponse, TimestampMixin):
    pass 