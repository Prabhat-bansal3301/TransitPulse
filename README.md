# TransitPulse

Real-time bus tracking and trip telemetry for public transport.

TransitPulse connects an Android tracking device to a FastAPI backend so operators can start trips and send GPS updates, while passenger-facing clients can read routes, buses, stops, trips, and the latest bus locations.

> **Project status:** Active prototype. The backend and Android tracker are under development; the passenger web frontend is not implemented yet.

## What is included

- **FastAPI backend** for buses, routes, stops, trips, and location telemetry
- **PostgreSQL + PostGIS schema** for transport and geospatial data
- **Device authentication** with hashed bearer tokens
- **Android tracker app** using Java, Retrofit, Fused Location Provider, and a foreground service
- **Operational scripts** for registering devices and rotating device tokens
- **API and product documentation** in [`docs/`](docs/)

## Architecture

```text
Android tracker
  └─ starts a trip and sends GPS telemetry
       │
       ▼
FastAPI REST API (/api/v1)
  ├─ public passenger read endpoints
  └─ authenticated tracker write endpoints
       │
       ▼
PostgreSQL + PostGIS
  ├─ buses, routes, stops, and route stops
  ├─ devices and active trips
  └─ historical GPS locations
```

## Repository layout

```text
backend/     FastAPI application, database access, schemas, and admin scripts
docs/        API, database, feature, product, roadmap, and stack documentation
frontend/    Reserved for the passenger web application
tracker/     Android tracking application
```

## Technology stack

| Area | Technologies |
| --- | --- |
| Backend | Python, FastAPI, Pydantic, Uvicorn |
| Database | PostgreSQL, PostGIS, Psycopg |
| Tracker | Java, Android SDK, Fused Location Provider, Retrofit |
| API format | Versioned REST API, JSON |
| Authentication | Bearer device tokens stored as SHA-256 hashes |

## Backend setup

### Requirements

- Python 3.10+
- PostgreSQL with the PostGIS extension
- A database created for TransitPulse

### Install dependencies

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Configure the database

The backend reads these variables from the environment or a `backend/.env` file:

```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=transitpulse
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
```

Apply the schema to a PostGIS-enabled database:

```bash
psql "$DATABASE_URL" -f backend/app/db/schema.sql
```

If `DATABASE_URL` is not configured in your shell, run `psql` with the connection options for your local PostgreSQL installation.

### Start the API

From the `backend/` directory:

```bash
uvicorn app.main:app --reload
```

The API is then available at `http://127.0.0.1:8000`.

- Health check: `GET /api/v1/health`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Device registration

Register a tracker device from the `backend/` directory:

```bash
python register_device.py <device_identifier> [bus_id]
```

The command prints the device token once. Store it securely; only its hash is persisted by the backend.

To rotate a device token, update the configured device ID in `backend/rotate_device_token.py` and run:

```bash
python rotate_device_token.py
```

## API overview

All current endpoints are versioned under `/api/v1`.

### Public read endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/health` | Check API availability |
| GET | `/buses` | List buses |
| GET | `/buses/{bus_id}` | Get a bus |
| GET | `/buses/{bus_id}/location` | Get the latest location for a bus |
| GET | `/routes` | List routes |
| GET | `/routes/{route_id}` | Get a route |
| GET | `/routes/{route_id}/stops` | List stops on a route |
| GET | `/stops` | List stops |
| GET | `/trips/active` | List active trips |
| GET | `/trips/{trip_id}` | Get a trip |

### Authenticated tracker endpoints

Send a device token in the request header:

```http
Authorization: Bearer <device-token>
```

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/trips` | Start a trip for a bus and route |
| POST | `/trips/{trip_id}/end` | End an active trip |
| POST | `/locations` | Submit GPS telemetry for an active trip |

Example location payload:

```json
{
  "trip_id": "00000000-0000-0000-0000-000000000000",
  "latitude": 29.8543,
  "longitude": 77.888,
  "recorded_at": "2026-11-11T16:00:00Z",
  "speed": 35.5
}
```

The backend validates coordinate ranges, requires a timezone-aware timestamp, and rejects timestamps more than two minutes in the future.

Administrative creation endpoints for buses, routes, and stops are currently available under `/api/v1/admin/`; see [`docs/API.md`](docs/API.md) for request details.

## Android tracker

The Android project is located at [`tracker/android/`](tracker/android/). It currently:

- Loads buses and routes from the backend
- Starts and ends trips through the API
- Runs GPS collection in an Android foreground service
- Sends latitude, longitude, speed, and UTC timestamps
- Adds a bearer token when configured

The emulator API URL defaults to:

```text
http://10.0.2.2:8000/
```

This maps to the host machine's port 8000 from an Android emulator. Change `BASE_URL` in `RetrofitClient.java` when using a physical device or a deployed API.

Open `tracker/android/` in Android Studio and run the `app` configuration. Location permissions and a reachable backend are required for live tracking.

## Data model

The database schema includes:

- Users and depots
- Buses and registered tracking devices
- Routes, stops, and ordered route stops
- Trips with `CREATED`, `ACTIVE`, and `COMPLETED` states
- GPS locations associated with trips

An enforced partial unique index prevents more than one active trip from running for the same bus.

## Documentation

- [`docs/API.md`](docs/API.md) — API contract and access model
- [`docs/DATABASE.md`](docs/DATABASE.md) — database design
- [`docs/FEATURES.md`](docs/FEATURES.md) — planned and implemented feature scope
- [`docs/PRD.md`](docs/PRD.md) — product requirements
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — development phases
- [`docs/TECHSTACK.md`](docs/TECHSTACK.md) — technology choices
- [`docs/USERFLOW.md`](docs/USERFLOW.md) — user flows

## Roadmap

- Improve device and admin authentication flows
- Add ETA calculation and route-aware arrival estimates
- Build the passenger web interface with live map updates
- Add an admin dashboard for buses, routes, stops, devices, and trips
- Add automated tests, deployment configuration, and monitoring

## Disclaimer

TransitPulse is an independent prototype. Integration with transport operators, vehicle tracking systems, ETM/POS devices, or production infrastructure requires authorization from the relevant organization.

## License

No license has been published for this repository yet.
