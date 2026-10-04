from fastapi import FastAPI
from app.db.bus import get_all_buses

app = FastAPI(title="TransitPulse API")


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/v1/buses")
def get_buses():
    buses = get_all_buses()

    return {
        "buses": buses
    }