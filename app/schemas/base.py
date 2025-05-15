from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TimestampMixin(BaseModel):
    created_at: datetime
    updated_at: datetime

class BaseResponse(BaseModel):
    id: int 