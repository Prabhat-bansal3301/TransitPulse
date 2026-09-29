# TransitPulse — User Flow

## 1. Passenger Flow

Open TransitPulse
        ↓
View Routes
        ↓
Select Route
        ↓
View Active Buses
        ↓
Select Bus
        ↓
View Live Bus Location
        ↓
Select Stop
        ↓
View ETA

## 2. Conductor / Tracker Flow
Open Tracker App
        ↓
Login / Authenticate
        ↓
Select Bus
        ↓
Select Route
        ↓
Start Journey
        ↓
Backend Creates Trip
        ↓
GPS Tracking Starts
        ↓
Send GPS Location Every 10–30 Seconds
        ↓
Continue Journey
        ↓
End Journey
        ↓
Backend Marks Trip as Completed


## 3. Admin Flow
Admin Login
      ↓
Manage Buses
      ↓
Manage Routes
      ↓
Manage Stops
      ↓
Register Tracking Devices
      ↓
Assign Device to Bus
      ↓
Monitor Active Journeys

## 4. Complete System Flow
Admin Configures Bus + Route + Device
                ↓
Conductor Selects Bus + Route
                ↓
Conductor Starts Journey
                ↓
Backend Creates Trip
                ↓
Android Tracker Collects GPS
                ↓
GPS Data Sent to Backend
                ↓
Backend Validates GPS Data
                ↓
Location Stored in Database
                ↓
Backend Processes Location / ETA
                ↓
Passenger Requests Bus Information
                ↓
Passenger Sees Bus Location + ETA
                ↓
Conductor Ends Journey
                ↓
Trip Marked as Completed

## 5. GPS Data Flow
Android Tracker
      ↓
GPS Coordinates
      ↓
HTTPS Request
      ↓
FastAPI Backend
      ↓
Authentication
      ↓
Validation
      ↓
PostgreSQL + PostGIS
      ↓
Latest Bus Location
      ↓
Passenger Web App

## 6. Trip Lifecycle

CREATED
   ↓
ACTIVE
   ↓
COMPLETED

- CREATED: Trip is created when the conductor starts a journey.
- ACTIVE: Bus is currently operating and sending GPS data.
- COMPLETED: Conductor ends the journey.

## 7. Failure Flow

### 7.1 Network Failure

Tracker
   ↓
Network Unavailable
   ↓
Retry Transmission

### 7.2 Invalid GPS Data

Tracker
   ↓
GPS Data
   ↓
Backend Validation
   ↓
Invalid → Reject

### 7.3 Tracker Offline

No Recent GPS Data
        ↓
Backend Detects Stale Location
        ↓
Passenger Sees Last Updated Time