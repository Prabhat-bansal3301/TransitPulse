
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class StopCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class StopResponse(BaseModel):
    id: UUID
    name: str
    latitude: float
    longitude: float
    is_active: bool
    created_at: datetime
