# TransitPulse — Features

## 1. Passenger Features

### 1.1 View Available Buses

Passengers can view buses currently available in the system.

The system may display:

- Bus number
- Route
- Current status
- Last updated time
- Current location

### 1.2 Live Bus Tracking

Passengers can view the current location of a bus on a map.

The location should be updated periodically as new GPS data is received from the tracking device.

### 1.3 Route Information

Passengers can view:

- Route name
- Starting point
- Destination
- Stops along the route
- Bus assigned to the route

### 1.4 Estimated Arrival Time

The system will provide an estimated arrival time for a bus at a selected stop.

The initial MVP may use a basic ETA calculation based on:

- Current bus location
- Destination/stop location
- Route information
- Current or estimated speed

More advanced ETA models can be introduced later.

### 1.5 Last Updated Information

The passenger should be able to see when the bus location was last received.

Example:

```text
Last updated: 15 seconds ago