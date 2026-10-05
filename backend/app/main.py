from uuid import UUID

from fastapi import FastAPI,HTTPException

from app.db.bus import get_all_buses, get_bus_by_id
from app.schemas.bus import BusResponse


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