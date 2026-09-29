# TransitPulse — Tech Stack

## 1. Frontend

### Passenger Web Application
- HTML
- CSS
- JavaScript
- Map integration

### Admin Dashboard
- HTML
- CSS
- JavaScript

The frontend will communicate with the backend through REST APIs.

---

## 2. Conductor / Tracker Application

- Java
- Android Studio
- Android SDK
- Android Location Services
- Fused Location Provider
- Retrofit for API communication
- Android Foreground Service for background GPS tracking

The Android application will act as the conductor interface and GPS tracking device for the MVP.

---

## 3. Backend

- Python
- FastAPI
- Pydantic
- REST API
- Uvicorn

FastAPI will handle:

- Authentication
- Bus management
- Route management
- Trip management
- GPS telemetry
- ETA processing
- Passenger APIs
- Admin APIs

---

## 4. Database

- PostgreSQL
- PostGIS

PostgreSQL will store application data.

PostGIS will provide geographical data support for:

- Bus locations
- Stops
- Routes
- GPS coordinates
- Spatial queries

---

## 5. API Communication

### Tracker → Backend
HTTPS
REST API
JSON

### Passenger → Backend
HTTPS
REST API
JSON

### Admin → Backend
HTTPS
REST API
JSON