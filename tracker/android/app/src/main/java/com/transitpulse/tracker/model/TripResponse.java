
package com.transitpulse.tracker.model;

import com.google.gson.annotations.SerializedName;

public class TripResponse {

    @SerializedName("trip_id")
    private String tripId;

    @SerializedName("status")
    private String status;

    public String getTripId() {
        return tripId;
    }

    public String getStatus() {
        return status;
    }
}