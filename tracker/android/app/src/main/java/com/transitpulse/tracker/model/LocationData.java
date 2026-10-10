package com.transitpulse.tracker.model;

import com.google.gson.annotations.SerializedName;

public class LocationData {

    @SerializedName("trip_id")
    private final String tripId;

    @SerializedName("latitude")
    private final double latitude;

    @SerializedName("longitude")
    private final double longitude;

    // Time when the device recorded the GPS measurement.
    @SerializedName("recorded_at")
    private final String recordedAt;

    // Speed is transmitted in kilometres per second (km/s).
    @SerializedName("speed")
    private final double speed;

    public LocationData(
            String tripId,
            double latitude,
            double longitude,
            String recordedAt,
            double speedKmh) {

        this.tripId = tripId;
        this.latitude = latitude;
        this.longitude = longitude;
        this.recordedAt = recordedAt;
        this.speed = speedKmh;
    }

    public String getTripId() {
        return tripId;
    }

    public double getLatitude() {
        return latitude;
    }

    public double getLongitude() {
        return longitude;
    }

    public String getRecordedAt() {
        return recordedAt;
    }

    public double getSpeed() {
        return speed;
    }
}

