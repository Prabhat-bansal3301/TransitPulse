
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

class BusCreate(BaseModel):
    bus_number: str = Field(min_length=1, max_length=50)
    operator: str | None = Field(default=None, max_length=100)
    depot_id: UUID | None = None

class BusResponse(BaseModel):
    id: UUID
    bus_number: str
    operator: str | None
    depot_id: UUID | None
    depot_name: str | None
    is_active: bool
    created_at: datetime
