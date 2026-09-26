# TransitPulse — Product Requirements Document

## 1. Product Overview

TransitPulse is a real-time public transport tracking and ETA platform designed to help passengers know the current location of their bus and its expected arrival time.

The system will collect location data from a GPS-enabled tracking device installed or operated inside a bus, transmit the data to a centralized backend, process the location information, and provide real-time bus information to passengers through a web platform.

The initial prototype will use an Android smartphone as the GPS tracking device. In future versions, TransitPulse may integrate with authorized transport-corporation systems, ETMs/POS devices, vehicle tracking systems, or other telemetry sources.

---

## 2. Problem Statement

Passengers often do not have reliable information about the current location or expected arrival time of public buses.

This can result in:

- Long and uncertain waiting times
- Difficulty knowing whether a bus has started its journey
- Difficulty tracking buses during a journey
- Lack of reliable real-time transport information
- Inefficient planning of daily travel

TransitPulse aims to address this problem by providing real-time bus location and estimated arrival information through a centralized platform.

---

## 3. Product Goal

The primary goal of TransitPulse is to provide passengers with accessible and reliable real-time information about public buses.

The initial MVP will demonstrate the complete data flow:

GPS Tracker → Backend → Database → Processing → Passenger Web Platform

---

## 4. Target Users

### 4.1 Passengers

Passengers use TransitPulse to:

- Find available buses
- View bus locations
- View routes and stops
- Track buses in real time
- View estimated arrival times

### 4.2 Transport Operators

Transport operators may use TransitPulse to:

- Register buses and tracking devices
- Monitor active vehicles
- View vehicle locations
- Manage routes and stops
- Monitor tracking status

### 4.3 System Administrators

Administrators manage:

- Users
- Buses
- Tracking devices
- Routes
- Stops
- System configuration
- Security and access control

---

## 5. MVP Scope

The initial MVP will include:

- Android-based GPS tracker
- Secure location transmission
- Backend REST API
- PostgreSQL database
- PostGIS spatial data support
- Bus and route management
- Real-time bus location
- Basic ETA calculation
- Passenger web interface
- Device authentication
- Basic API security
- Logging and monitoring

---

## 6. Out of Scope for MVP

The following features will not be required for the initial MVP:

- Native passenger Android application
- Native passenger iOS application
- Payment or ticketing
- Online ticket booking
- Integration with real transport-corporation ETM/POS systems
- Large-scale production deployment
- Advanced machine-learning-based ETA prediction
- Automated fleet scheduling

These features may be considered in future versions.

---

## 7. Product Requirements

### 7.1 Passenger Requirements

The system should allow passengers to:

- View available buses
- Select a bus or route
- View the current bus location
- View route information
- View estimated arrival time
- View the last known location update

### 7.2 Tracker Requirements

The tracking device should:

- Obtain GPS coordinates
- Send location data to the backend
- Include device identification
- Include timestamp information
- Continue tracking when the application is running in the background
- Handle temporary network failures

### 7.3 Backend Requirements

The backend should:

- Authenticate tracking devices
- Receive GPS location data
- Validate incoming data
- Store location information
- Process bus locations
- Provide bus and route information
- Provide ETA information
- Expose APIs for the frontend
- Support real-time updates

### 7.4 Database Requirements

The database should store:

- Users
- Buses
- Tracking devices
- Routes
- Stops
- Trips
- GPS locations
- Relevant timestamps and status information

The database should support geographical queries using PostGIS.

---

## 8. Security Requirements

TransitPulse should implement basic security controls from the beginning.

The system should:

- Authenticate tracking devices
- Use HTTPS for communication
- Validate incoming API requests
- Prevent unauthorized devices from submitting telemetry
- Validate GPS coordinates and timestamps
- Apply rate limiting where appropriate
- Protect administrative endpoints
- Log important security events

Future versions may include stronger telemetry integrity and GPS-spoofing detection.

---

## 9. Non-Functional Requirements

### Performance

The system should process location updates with low latency suitable for real-time tracking.

### Reliability

Temporary network failures should not permanently break tracking.

### Scalability

The backend architecture should allow additional buses, routes, and tracking devices to be added later.

### Security

Sensitive communication and system operations should be protected against unauthorized access.

### Maintainability

The system should use a modular architecture so that the tracker, backend, database, and frontend can be developed and maintained independently.

### Extensibility

The backend should be designed so that the initial Android tracker can eventually be replaced or supplemented by authorized vehicle telemetry or ETM/POS integrations.

---

## 10. Assumptions and Constraints

### Assumptions

- The tracking device has GPS capability.
- The tracking device has mobile internet or another network connection.
- The backend server is reachable by the tracking device.
- Initial tracking data will come from an Android smartphone.
- Transport-system integrations in future versions will require appropriate authorization.

### Constraints

- The initial project is a student MVP.
- Development time is limited.
- Initial testing may use simulated or controlled bus routes.
- GPS accuracy may vary depending on environmental conditions.
- ETA accuracy will depend on available route, location, and traffic data.

---

## 11. Success Criteria

The MVP will be considered successful when:

1. An Android device can obtain its GPS location.
2. The device can securely transmit its location to the backend.
3. The backend can validate and store the location.
4. The passenger web platform can retrieve the bus location.
5. The bus can be displayed on a map.
6. The system can provide a basic ETA.
7. The complete tracking flow works reliably during a live demonstration.

---

## 12. Future Scope

Future versions of TransitPulse may include:

- Integration with authorized ETM/POS systems
- Integration with transport-corporation APIs
- Native passenger mobile applications
- Advanced ETA prediction
- Historical route analytics
- Fleet monitoring
- Driver/operator dashboards
- Notifications for approaching buses
- Route disruption alerts
- GPS-spoofing detection
- Large-scale multi-city deployment