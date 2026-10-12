
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class BusResponse(BaseModel):
    id: UUID
    bus_number: str
    operator: str | None
    depot_id: UUID | None
    depot_name: str | None
    is_active: bool
    created_at: datetime
