from pydantic import BaseModel
from .base import TimestampMixin, BaseResponse

class CategoryBase(BaseModel):
    name: str
    description: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase, BaseResponse, TimestampMixin):
    id: int 