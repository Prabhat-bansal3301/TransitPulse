# TransitPulse — Database Design

## 1. Database Overview

TransitPulse uses:

- PostgreSQL
- PostGIS

PostgreSQL stores the main application data.

PostGIS is used for geographic data such as:

- Bus locations
- Stop locations
- Route geometry
- Spatial queries

The database is designed around buses, routes, trips, stops, devices, users, and GPS telemetry.

---

## 2. Main Entities

The MVP database contains the following main entities:

```text
users
buses
devices
routes
stops
route_stops
trips
locations
```

---

## 3. Entity Relationships

The main relationship is:

```text
User
 │
 ├── Conductor
 └── Admin


Bus
 │
 └── Device


Route
 │
 └── Route Stops
        │
        └── Stops


Bus + Route + Device
        │
        ▼
       Trip
        │
        ▼
    GPS Locations
```

A trip represents one actual journey of a bus on a route.

Example:

```text
Bus:
UK08AB1234

Route:
Roorkee → Dehradun

Trip:
#9821

GPS Locations:
Location 1
Location 2
Location 3
...
```

---

# 4. Users Table

The `users` table stores authenticated system users.

Passengers do not need accounts in the MVP.

### Fields

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| name | VARCHAR | User name |
| email | VARCHAR | Login email |
| password_hash | VARCHAR | Hashed password |
| role | VARCHAR | `ADMIN` or `CONDUCTOR` |
| is_active | BOOLEAN | Account status |
| created_at | TIMESTAMP | Account creation time |

### Roles

```text
ADMIN
CONDUCTOR
```

Role-based access control is handled by the backend.

---

# 5. Buses Table

The `buses` table stores registered buses.

### Fields

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| bus_number | VARCHAR | Bus registration/identifier |
| operator | VARCHAR | Transport operator |
| is_active | BOOLEAN | Bus status |
| created_at | TIMESTAMP | Creation time |

Example:

```text
id: bus-101
bus_number: UK08AB1234
operator: UTC
is_active: true
```

---

# 6. Devices Table

The `devices` table stores tracker devices used by buses.

For the MVP, the tracker device can be an Android phone running the Conductor/Tracker application.

### Fields

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| device_identifier | VARCHAR | Unique device identifier |
| device_token_hash | VARCHAR | Stored authentication token hash |
| bus_id | UUID | Assigned bus |
| is_active | BOOLEAN | Device status |
| last_seen_at | TIMESTAMP | Last communication time |
| created_at | TIMESTAMP | Creation time |

### Relationship

```text
Bus 1 ─────── 1 Device
```

A device can be assigned to a bus.

The exact assignment rules can be refined during implementation.

---

# 7. Routes Table

The `routes` table stores permanent bus routes.

A route is not a specific journey.

Example:

```text
Route #12
Roorkee → Dehradun
```

### Fields

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| route_code | VARCHAR | Human-readable route identifier |
| name | VARCHAR | Route name |
| description | TEXT | Optional route description |
| is_active | BOOLEAN | Route status |
| created_at | TIMESTAMP | Creation time |

Example:

```text
route_id: route-12
route_code: RKR-DDN-01
name: Roorkee → Dehradun
```

---

# 8. Stops Table

The `stops` table stores physical bus stops.

### Fields

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| name | VARCHAR | Stop name |
| latitude | DOUBLE PRECISION | Latitude |
| longitude | DOUBLE PRECISION | Longitude |
| location | GEOGRAPHY(Point, 4326) | PostGIS location |
| is_active | BOOLEAN | Stop status |
| created_at | TIMESTAMP | Creation time |

PostGIS allows the system to perform geographic calculations using the stop location.

Example:

```text
Stop:
Roorkee Bus Stand

Latitude:
29.8543

Longitude:
77.8880
```

---

# 9. Route Stops Table

A route can contain multiple stops, and a stop can potentially belong to multiple routes.

Therefore, the relationship between routes and stops is many-to-many.

The `route_stops` table connects them.

### Fields

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| route_id | UUID | Route reference |
| stop_id | UUID | Stop reference |
| stop_sequence | INTEGER | Position of stop on route |
| created_at | TIMESTAMP | Creation time |

Example:

```text
Route #12

1. Roorkee Bus Stand
2. Manglaur
3. Muzaffarnagar
4. Meerut
5. Dehradun
```

The `stop_sequence` field preserves the order of stops.

---

# 10. Trips Table

The `trips` table is one of the most important tables in TransitPulse.

A route is permanent, while a trip represents one actual journey.

Example:

```text
Route #12
        +
Bus #101
        +
Start at 07:30
        ↓
Trip #9821
```

### Fields

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| bus_id | UUID | Bus reference |
| route_id | UUID | Route reference |
| device_id | UUID | Tracker device reference |
| conductor_id | UUID | User/conductor reference |
| status | VARCHAR | Trip status |
| started_at | TIMESTAMP | Journey start time |
| completed_at | TIMESTAMP | Journey completion time |
| created_at | TIMESTAMP | Trip creation time |

### Trip Status

```text
CREATED
ACTIVE
COMPLETED
```

The normal lifecycle is:

```text
CREATED
   ↓
ACTIVE
   ↓
COMPLETED
```

---

# 11. Locations Table

The `locations` table stores GPS telemetry received from the tracker application.

Each location belongs to a specific trip.

### Fields

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| trip_id | UUID | Trip reference |
| latitude | DOUBLE PRECISION | GPS latitude |
| longitude | DOUBLE PRECISION | GPS longitude |
| location | GEOGRAPHY(Point, 4326) | PostGIS point |
| speed | DOUBLE PRECISION | Speed reported by device |
| recorded_at | TIMESTAMP | Time GPS was recorded |
| received_at | TIMESTAMP | Time backend received data |

Example:

```text
Trip:
9821

Location:
Latitude: 29.8543
Longitude: 77.8880
Speed: 35.5 km/h
Recorded: 10:30:00
```

---

# 12. Why Store Both Recorded and Received Time?

The tracker may collect GPS data when the network is temporarily unavailable.

For example:

```text
10:30:00
GPS recorded

10:30:08
Network available

10:30:09
Backend receives data
```

Therefore:

```text
recorded_at = 10:30:00
received_at = 10:30:09
```

This helps distinguish the actual GPS time from the server reception time.

---

# 13. Foreign Key Relationships

The major relationships are:

```text
devices.bus_id
        ↓
      buses.id


route_stops.route_id
        ↓
      routes.id


route_stops.stop_id
        ↓
      stops.id


trips.bus_id
        ↓
      buses.id


trips.route_id
        ↓
      routes.id


trips.device_id
        ↓
      devices.id


trips.conductor_id
        ↓
      users.id


locations.trip_id
        ↓
      trips.id
```

---

# 14. Complete Database Relationship

```text
                    ┌──────────────┐
                    │    USERS     │
                    │              │
                    │ ADMIN        │
                    │ CONDUCTOR    │
                    └──────┬───────┘
                           │
                           │ conductor_id
                           ▼
                    ┌──────────────┐
                    │    TRIPS     │
                    └──────┬───────┘
                           │
                           │ trip_id
                           ▼
                    ┌──────────────┐
                    │  LOCATIONS   │
                    │              │
                    │ GPS data     │
                    └──────────────┘


┌──────────────┐
│    BUSES     │
└──────┬───────┘
       │
       ├───────────────┐
       │               │
       ▼               ▼
┌──────────────┐  ┌──────────────┐
│   DEVICES    │  │    TRIPS     │
└──────────────┘  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │    ROUTES    │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ ROUTE_STOPS  │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │    STOPS     │
                  └──────────────┘
```

---

# 15. Passenger Data Flow

Passengers do not directly access the database.

The flow is:

```text
Passenger Web App
       │
       │ REST API
       ▼
   FastAPI Backend
       │
       │ SQL / PostGIS
       ▼
 PostgreSQL + PostGIS
```

Example:

```text
Passenger requests:

GET /api/v1/routes
```

Backend queries:

```text
routes
```

Then returns JSON.

---

# 16. Live Bus Location Flow

The tracker sends GPS data:

```text
Android Tracker
      │
      │ POST /locations
      ▼
FastAPI Backend
      │
      │ Validate
      ▼
   locations
      │
      ▼
PostgreSQL + PostGIS
```

Passenger requests bus location:

```text
GET /api/v1/buses/{bus_id}/location
```

Backend finds the active trip and latest valid location.

---

# 17. Trip and GPS Relationship

One trip can have many GPS locations.

```text
Trip #9821
    │
    ├── Location #1
    ├── Location #2
    ├── Location #3
    ├── Location #4
    └── Location #5
```

Therefore:

```text
trips 1 ─────────── N locations
```

This is important because GPS updates may arrive every 10–30 seconds.

---

# 18. Route and Stop Relationship

One route contains multiple stops.

A stop can belong to multiple routes.

Therefore:

```text
routes N ───────── N stops
```

The relationship is implemented using:

```text
route_stops
```

Example:

```text
Route 12
    │
    ├── Stop 1
    ├── Stop 2
    ├── Stop 3
    └── Stop 4
```

---

# 19. PostGIS Usage

PostGIS will be used for geographic operations.

Examples:

### Bus Location

```text
POINT(longitude latitude)
```

### Stop Location

```text
POINT(longitude latitude)
```

PostGIS can later be used for:

- Distance between bus and stop
- Finding nearby stops
- Route proximity checks
- GPS validation
- Route deviation detection
- Spatial queries

---

# 20. GPS Validation

The backend should validate incoming GPS data before storing it.

Basic validation includes:

```text
Latitude:
-90 to +90

Longitude:
-180 to +180
```

The backend should also validate:

- authenticated device
- valid trip
- trip is ACTIVE
- valid timestamp
- required fields
- reasonable GPS values

Invalid telemetry should be rejected.

---

# 21. Database Indexing

Indexes should be added to frequently queried fields.

Important indexes include:

```text
users.email

buses.bus_number

devices.device_identifier

trips.bus_id

trips.route_id

trips.status

locations.trip_id

locations.recorded_at

route_stops.route_id

route_stops.stop_id
```

A spatial index should also be used for PostGIS location columns.

---

# 22. Data Integrity

The database should enforce relationships using:

- Primary keys
- Foreign keys
- Unique constraints
- NOT NULL constraints
- CHECK constraints where appropriate

Examples:

```text
bus_number → unique

device_identifier → unique

users.email → unique

latitude → valid range

longitude → valid range
```

---

# 23. MVP Database Scope

The MVP database focuses on:

```text
Users
Buses
Devices
Routes
Stops
Route Stops
Trips
GPS Locations
```

The design intentionally avoids unnecessary tables and complex functionality during the first implementation.

---

# 24. Future Database Extensions

Future versions may add:

```text
trip_history
notifications
fare_information
fleet_analytics
vehicle_maintenance
gps_anomalies
route_versions
traffic_data
etm_devices
transport_operator_integrations
```

These should only be added when the corresponding features are actually implemented.

---

# 25. Database Architecture Summary

```text
                    TransitPulse
                         │
                         ▼
              PostgreSQL + PostGIS
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
     Users             Buses            Routes
       │                 │                 │
       │                 ▼                 ▼
       │              Devices         Route Stops
       │                                   │
       │                                   ▼
       │                                  Stops
       │
       └─────────────────┐
                         ▼
                       Trips
                         │
                         ▼
                     Locations
                         │
                         ▼
                     GPS Data
```

The database provides the persistent data layer for the TransitPulse backend and supports the Passenger Web App, Conductor/Tracker Android App, and Admin Dashboard through the FastAPI REST API.
