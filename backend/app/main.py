from uuid import UUID
from fastapi import FastAPI,HTTPException, status
from psycopg.errors import ForeignKeyViolation, UniqueViolation

from app.db.bus import get_all_buses, get_bus_by_id, create_bus
from app.schemas.bus import BusResponse, BusCreate


app = FastAPI(title="TransitPulse API")


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/v1/buses", response_model=list[BusResponse])
def get_buses():
    return get_all_buses()


@app.get("/api/v1/buses/{bus_id}", response_model=BusResponse)
def get_bus(bus_id: UUID):
    bus = get_bus_by_id(bus_id)

    if bus is None:
        raise HTTPException(status_code=404, detail="Bus not found")

    return bus


@app.post(
    "/api/v1/admin/buses",
    response_model=BusResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_bus(bus_data: BusCreate):
    try:
        return create_bus(
            bus_number=bus_data.bus_number,
            operator=bus_data.operator,
            depot_id=bus_data.depot_id,
        )
    except Exception as exc:
        if isinstance(exc, UniqueViolation):
            raise HTTPException(
                status_code=409,
                detail="A bus with this bus number already exists",
            ) from exc

        if isinstance(exc, ForeignKeyViolation):
            raise HTTPException(
                status_code=400,
                detail="The specified depot does not exist",
            ) from exc

        raise
