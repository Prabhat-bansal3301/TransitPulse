
package com.transitpulse.tracker.model;

import com.google.gson.annotations.SerializedName;

public class StartTripRequest {

    @SerializedName("bus_id")
    private final String busId;

    @SerializedName("route_id")
    private final String routeId;

    public StartTripRequest(String busId, String routeId) {
        this.busId = busId;
        this.routeId = routeId;
    }
}