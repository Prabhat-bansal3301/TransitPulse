# TransitPulse 🚌

**Real-Time Public Transport Tracking & ETA Platform**

TransitPulse is a real-time public transport tracking platform designed to help passengers know **where a bus is, whether it is approaching, and approximately when it will arrive**.

The initial goal is to solve a common problem with regular public buses: passengers often have little or no reliable information about the current location of their bus, resulting in long and uncertain waiting times.

## 🎯 Problem

Many public transport systems do not provide reliable real-time tracking for all buses, particularly regular/non-premium services.

Passengers may have to wait at a bus stop for a long time without knowing:

* Where the bus currently is
* Whether the bus has started its route
* Whether it is approaching their stop
* When it is expected to arrive
* Whether they should wait or choose another mode of transport

TransitPulse aims to provide this information through a simple web platform.

## 💡 Proposed Solution

TransitPulse will collect the real-time GPS location of a bus and send it to a central backend.

The system will process the location data and provide passengers with:

* Live bus location
* Route information
* Last location update
* Estimated Time of Arrival (ETA)
* Bus activity/status

### Initial Prototype

For the prototype, an Android phone will act as the vehicle's GPS tracking device.

```text
Android GPS Tracker
        ↓
   Internet / API
        ↓
 Python Backend
        ↓
 PostgreSQL/PostGIS
        ↓
 ETA / Location Engine
        ↓
 Passenger Web Platform
```

In a future production implementation, the Android tracker could be replaced or integrated with an existing **ETM/POS/vehicle tracking system** used by a transport corporation, subject to access and authorization from the transport operator.

## 🏗️ Project Architecture

```text
┌─────────────────────┐
│   GPS Tracker       │
│   Android / ETM     │
└──────────┬──────────┘
           │
           │ Location Data
           ▼
┌─────────────────────┐
│   FastAPI Backend   │
│   Python            │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ PostgreSQL +        │
│ PostGIS             │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Location / ETA      │
│ Processing Engine   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Passenger Web App   │
│ Maps + Bus Status   │
└─────────────────────┘
```

## 🛠️ Technology Stack

### Backend

* Python
* FastAPI
* REST API
* WebSockets / real-time communication

### Database

* PostgreSQL
* PostGIS

### GPS Tracker

* Android
* Java
* Android Location APIs

### Frontend

* HTML
* CSS
* JavaScript
* Map API

### Infrastructure

* Linux
* Docker
* Git & GitHub

### Security

Security will be considered throughout the system, including:

* API authentication
* Device authentication
* Secure communication
* Input validation
* Rate limiting
* Protection against unauthorized location submissions
* Detection/mitigation of manipulated GPS data

## 🚧 Current Status

**Project Stage: Planning / Initial Development**

The current project is a prototype and is **not yet connected to any transport corporation's production systems**.

The initial implementation will use a controlled Android GPS tracker to simulate the data source that could eventually be provided by a vehicle tracking system or ETM/POS device.

## 🗺️ Future Roadmap

* [ ] Project architecture
* [ ] Backend API
* [ ] Database design
* [ ] Android GPS tracker
* [ ] Live location ingestion
* [ ] Passenger web interface
* [ ] Interactive map
* [ ] Route management
* [ ] ETA calculation
* [ ] Real-time updates
* [ ] Authentication & authorization
* [ ] Security testing
* [ ] Cloud deployment
* [ ] Performance testing
* [ ] Transport corporation integration
* [ ] Dedicated passenger mobile application

## 👥 Team

TransitPulse is being developed as a two-person project.

* **Developer 1:** Backend, cybersecurity, infrastructure & system architecture
* **Developer 2:** Android/Java, GPS tracking & mobile development

## ⚠️ Disclaimer

TransitPulse is currently an independent prototype.

Any future integration with transport corporations, ETM/POS devices, vehicle tracking systems, or their backend infrastructure will require appropriate authorization and cooperation from the respective organization.

---

**TransitPulse — Know your bus. Know when it's coming.**
