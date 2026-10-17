from uuid import UUID
from fastapi import FastAPI,HTTPException, status
from app.schemas.bus import BusResponse, BusCreate
from app.db.stop import get_all_stops, create_stop
from app.schemas.stop import StopCreate, StopResponse
from psycopg.errors import ForeignKeyViolation, UniqueViolation
from app.db.bus import get_all_buses, get_bus_by_id, create_bus
from app.schemas.route import RouteResponse, RouteCreate, RouteStopCreate
from app.db.route import get_all_routes, create_route, get_route_by_id, add_stop_to_route, get_stops_for_route
from app.db.trip import create_trip,get_trip_by_id,get_active_trips,end_trip
from pydantic import BaseModel
from app.db.location import create_location,get_latest_location_for_bus
from app.schemas.location import LocationCreate

app = FastAPI(title="TransitPulse API")

class TripCreate(BaseModel):
    bus_id: UUID
    route_id: UUID

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

@app.get("/api/v1/routes", response_model=list[RouteResponse])
def get_routes():
    return get_all_routes()

@app.get("/api/v1/routes/{route_id}", response_model=RouteResponse)
def get_route(route_id: UUID):
    route = get_route_by_id(route_id)

    if route is None:
        raise HTTPException(
            status_code=404,
            detail="Route not found",
        )

    return route


@app.get("/api/v1/stops", response_model=list[StopResponse])
def get_stops():
    return get_all_stops()



@app.get("/api/v1/routes/{route_id}/stops")
def get_route_stops(route_id: UUID):
    route = get_route_by_id(route_id)

    if route is None:
        raise HTTPException(
            status_code=404,
            detail="Route not found",
        )

    return get_stops_for_route(route_id)


@app.get("/api/v1/trips/active")
def read_active_trips():
    trips = get_active_trips()

    return [
        {
            "trip_id": trip["id"],
            "bus_id": trip["bus_id"],
            "route_id": trip["route_id"],
            "device_id": trip["device_id"],
            "conductor_id": trip["conductor_id"],
            "status": trip["status"],
            "started_at": trip["started_at"],
            "completed_at": trip["completed_at"],
            "created_at": trip["created_at"],
        }
        for trip in trips
    ]

@app.get("/api/v1/trips/{trip_id}")
def read_trip(trip_id: UUID):
    trip = get_trip_by_id(trip_id)

    if trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found.",
        )

    return {
        "trip_id": trip["id"],
        "bus_id": trip["bus_id"],
        "route_id": trip["route_id"],
        "device_id": trip["device_id"],
        "conductor_id": trip["conductor_id"],
        "status": trip["status"],
        "started_at": trip["started_at"],
        "completed_at": trip["completed_at"],
        "created_at": trip["created_at"],
    }

@app.get("/api/v1/buses/{bus_id}/location")
def read_latest_bus_location(bus_id: UUID):
    location = get_latest_location_for_bus(bus_id)

    if location is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No location found for this bus's active trip.",
        )

    return location
    

@app.post(
    "/api/v1/admin/stops",
    response_model=StopResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_stop(stop_data: StopCreate):
    return create_stop(
        name=stop_data.name,
        latitude=stop_data.latitude,
        longitude=stop_data.longitude,
    )


@app.post(
    "/api/v1/admin/routes",
    response_model=RouteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_route(route_data: RouteCreate):
    try:
        return create_route(
            route_code=route_data.route_code,
            name=route_data.name,
            description=route_data.description,
        )
    except UniqueViolation as exc:
        raise HTTPException(
            status_code=409,
            detail="A route with this route code already exists",
        ) from exc

@app.post(
    "/api/v1/admin/routes/{route_id}/stops",
    status_code=status.HTTP_201_CREATED,
)
def assign_stop_to_route(
    route_id: UUID,
    stop_data: RouteStopCreate,
):
    try:
        return add_stop_to_route(
            route_id=route_id,
            stop_id=stop_data.stop_id,
            stop_sequence=stop_data.stop_sequence,
        )
    except ForeignKeyViolation as exc:
        raise HTTPException(
            status_code=400,
            detail="The specified route or stop does not exist",
        ) from exc

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


@app.post("/api/v1/trips", status_code=status.HTTP_201_CREATED)
def start_trip(trip_data: TripCreate):
    try:
        trip = create_trip(
            bus_id=trip_data.bus_id,
            route_id=trip_data.route_id,
        )
        return {
            "trip_id": trip["id"],
            "bus_id": trip["bus_id"],
            "route_id": trip["route_id"],
            "status": trip["status"],
            "started_at": trip["started_at"],
        }
    except UniqueViolation:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This bus already has an active trip.",
        )
    except ForeignKeyViolation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The specified bus or route does not exist.",
        )

    
@app.post("/api/v1/trips/{trip_id}/end")
def finish_trip(trip_id: UUID):
    trip = end_trip(trip_id)

    if trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found or is not active.",
        )

    return {
        "trip_id": trip["id"],
        "bus_id": trip["bus_id"],
        "route_id": trip["route_id"],
        "status": trip["status"],
        "started_at": trip["started_at"],
        "completed_at": trip["completed_at"],
    }


@app.post("/api/v1/locations", status_code=status.HTTP_201_CREATED)
def submit_location(location_data: LocationCreate):
    location = create_location(
        trip_id=location_data.trip_id,
        latitude=location_data.latitude,
        longitude=location_data.longitude,
        recorded_at=location_data.recorded_at,
        speed=location_data.speed,
    )

    if location is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found or is not active.",
        )

    return {
        "success": True,
        "location_id": location["id"],
        "trip_id": location["trip_id"],
        "recorded_at": location["recorded_at"],
        "received_at": location["received_at"],
    }
