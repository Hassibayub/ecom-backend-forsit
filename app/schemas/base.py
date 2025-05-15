from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class TimestampMixin(BaseModel):
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class BaseResponse(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True) 