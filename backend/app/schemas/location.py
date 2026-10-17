
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class LocationCreate(BaseModel):
    trip_id: UUID
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    recorded_at: datetime
    speed: float | None = Field(default=None, ge=0)
