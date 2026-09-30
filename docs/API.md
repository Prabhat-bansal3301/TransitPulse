# TransitPulse — API Documentation

## 1. API Overview

TransitPulse uses a REST API to connect the Passenger Web Application, Conductor/Tracker Android Application, and Admin Dashboard with the backend.

The backend is built using FastAPI.

### Access Model

- Passenger → Public read-only APIs
- Conductor/Tracker → Authenticated APIs
- Admin → Authenticated and authorized APIs
- Passenger users do not need to sign up or log in.

---

## 2. API Versioning

All MVP APIs use:

```text
/api/v1
```

Example:

```text
GET /api/v1/routes
```

---

## 3. Authentication

### Passenger

No authentication is required for public passenger information.

### Conductor / Tracker

The tracker application must authenticate before performing protected operations.

### Admin

Administrative APIs require authentication and authorization.

---

## 4. Passenger APIs

### Get Routes

```text
GET /api/v1/routes
```

Returns available routes.

### Get Route Details

```text
GET /api/v1/routes/{route_id}
```

Returns route details and stops.

### Get Active Buses

```text
GET /api/v1/buses
```

Returns available/active buses.

### Get Bus Details

```text
GET /api/v1/buses/{bus_id}
```

Returns information about a specific bus.

### Get Bus Location

```text
GET /api/v1/buses/{bus_id}/location
```

Returns the latest known location of a bus.

### Get Bus ETA

```text
GET /api/v1/buses/{bus_id}/eta
```

Returns the estimated arrival time for a bus.

---

## 5. Conductor / Tracker APIs

### Get Assigned Buses

```text
GET /api/v1/tracker/buses
```

Returns buses available to the authenticated tracker/conductor.

### Get Available Routes

```text
GET /api/v1/tracker/routes
```

Returns routes available to the authenticated tracker/conductor.

### Start Journey

```text
POST /api/v1/trips
```

Creates a new Trip.

Request:

```json
{
  "bus_id": "bus-id",
  "route_id": "route-id"
}
```

Response:

```json
{
  "trip_id": "trip-id",
  "status": "ACTIVE"
}
```

### Send GPS Location

```text
POST /api/v1/locations
```

Sends GPS telemetry for an active Trip.

Request:

```json
{
  "trip_id": "trip-id",
  "latitude": 29.8543,
  "longitude": 77.8880,
  "timestamp": "2026-09-30T10:30:00Z",
  "speed": 35.5
}
```

Response:

```json
{
  "success": true
}
```

### End Journey

```text
POST /api/v1/trips/{trip_id}/end
```

Ends the active Trip and marks it as `COMPLETED`.

---

## 6. Trip APIs

### Get Trip

```text
GET /api/v1/trips/{trip_id}
```

Returns information about a specific Trip.

### Get Active Trips

```text
GET /api/v1/trips/active
```

Returns currently active bus journeys.

---

## 7. GPS / Location APIs

GPS telemetry is submitted by authenticated tracker devices.

A location update contains:

```json
{
  "trip_id": "trip-id",
  "latitude": 29.8543,
  "longitude": 77.8880,
  "timestamp": "2026-09-30T10:30:00Z",
  "speed": 35.5
}
```

The backend validates:

- Authentication
- Trip ID
- Trip status
- Latitude
- Longitude
- Timestamp
- Required fields

Invalid telemetry is rejected.

---

## 8. ETA APIs

### Get ETA

```text
GET /api/v1/buses/{bus_id}/eta
```

The MVP ETA may use:

- Current bus location
- Route information
- Stop location
- Current/estimated speed

Advanced traffic-aware and machine-learning-based ETA is future scope.

---

## 9. Admin APIs

All admin APIs require authentication and authorization.

### Create Bus

```text
POST /api/v1/admin/buses
```

### Get Buses

```text
GET /api/v1/admin/buses
```

### Update Bus

```text
PUT /api/v1/admin/buses/{bus_id}
```

### Create Route

```text
POST /api/v1/admin/routes
```

### Update Route

```text
PUT /api/v1/admin/routes/{route_id}
```

### Create Stop

```text
POST /api/v1/admin/stops
```

### Update Stop

```text
PUT /api/v1/admin/stops/{stop_id}
```

### Register Device

```text
POST /api/v1/admin/devices
```

### Assign Device to Bus

```text
PUT /api/v1/admin/buses/{bus_id}/device
```

### View Active Trips

```text
GET /api/v1/admin/trips/active
```

---

## 10. Request and Response Format

The API uses JSON for request and response bodies.

```http
Content-Type: application/json
```

---

## 11. HTTP Status Codes

```text
200 OK
201 Created
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Unprocessable Entity
429 Too Many Requests
500 Internal Server Error
```

---

## 12. Security Rules

The API should:

- Use HTTPS
- Authenticate tracker requests
- Authenticate admin requests
- Apply authorization to protected resources
- Validate all incoming data
- Validate GPS coordinates
- Validate timestamps
- Apply rate limiting
- Never expose sensitive credentials
- Log important security events

---

## 13. Future API Extensions

Future versions may include:

- Notifications
- Historical trip data
- Fleet analytics
- Traffic-aware ETA
- ETM/POS integration
- Transport-corporation integrations
- Advanced GPS spoofing detection
```

