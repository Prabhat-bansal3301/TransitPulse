package com.transitpulse.tracker.api;

import com.google.gson.JsonElement;
import com.transitpulse.tracker.model.LocationData;
import com.transitpulse.tracker.model.StartTripRequest;
import com.transitpulse.tracker.model.TripResponse;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.Path;

public interface ApiService {

    // Fetch buses, including their backend UUIDs.
    @GET("api/v1/tracker/buses")
    Call<JsonElement> getBuses();

    // Fetch routes, including their backend UUIDs.
    @GET("api/v1/tracker/routes")
    Call<JsonElement> getRoutes();

    // Create a Trip. The backend generates the official trip_id.
    @POST("api/v1/trips")
    Call<TripResponse> createTrip(
            @Body StartTripRequest request
    );

    // Submit GPS telemetry for an existing Trip.
    @POST("api/v1/locations")
    Call<JsonElement> sendLocation(
            @Body LocationData locationData
    );

    // End an existing Trip.
    @POST("api/v1/trips/{trip_id}/end")
    Call<JsonElement> endTrip(
            @Path("trip_id") String tripId
    );
}

