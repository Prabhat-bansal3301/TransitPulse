
from datetime import datetime, timedelta, timezone
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class LocationCreate(BaseModel):
    trip_id: UUID
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    recorded_at: datetime
    speed: float | None = Field(default=None, ge=0)

    @field_validator("recorded_at")
    @classmethod
    def validate_recorded_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError(
                "recorded_at must include a timezone, such as Z or +05:30."
            )

        now = datetime.now(timezone.utc)

        if value > now + timedelta(minutes=2):
            raise ValueError(
                "recorded_at cannot be more than 2 minutes in the future."
            )

        return value
