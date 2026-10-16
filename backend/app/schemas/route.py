
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel,Field

class RouteCreate(BaseModel):
    route_code: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None

class RouteResponse(BaseModel):
    id: UUID
    route_code: str
    name: str
    description: str | None
    is_active: bool
    created_at: datetime

class RouteStopCreate(BaseModel):
    stop_id: UUID
    stop_sequence: int = Field(ge=1)
