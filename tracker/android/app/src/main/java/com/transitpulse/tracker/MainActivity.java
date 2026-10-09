package com.transitpulse.tracker;

import android.Manifest;
import android.content.BroadcastReceiver;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.transitpulse.tracker.api.ApiService;
import com.transitpulse.tracker.api.RetrofitClient;
import com.transitpulse.tracker.model.StartTripRequest;
import com.transitpulse.tracker.model.TripResponse;

import java.util.ArrayList;
import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {

    private TextView locationText;
    private TextView journeyText;
    private Button startTrackingButton;
    private Button stopTrackingButton;

    private Spinner busSpinner;
    private Spinner routeSpinner;

    private ApiService apiService;

    // Backend UUIDs, kept separately from the displayed labels.
    private final List<String> busIds = new ArrayList<>();
    private final List<String> routeIds = new ArrayList<>();

    private String tripId;
    private boolean tripRequestInProgress = false;
    private boolean endRequestInProgress = false;

    private static final int LOCATION_PERMISSION_REQUEST_CODE = 100;

    private final BroadcastReceiver locationReceiver =
            new BroadcastReceiver() {
                @Override
                public void onReceive(
                        android.content.Context context,
                        Intent intent) {

                    double latitude =
                            intent.getDoubleExtra("latitude", 0);

                    double longitude =
                            intent.getDoubleExtra("longitude", 0);

                    float accuracy =
                            intent.getFloatExtra("accuracy", 0);


                    // LocationService already sends speed in km/h.
                    float speedKmh = intent.getFloatExtra("speed", 0);
                    String locationInfo =
                            "Tracking...\n\n" +
                                    "Latitude: " + latitude +
                                    "\nLongitude: " + longitude +
                                    "\nAccuracy: " + accuracy + " meters" +
                                    "\nSpeed: " + speedKmh + " km/s";

                    locationText.setText(locationInfo);
                }
            };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        locationText = findViewById(R.id.locationText);
        journeyText = findViewById(R.id.journeyText);
        startTrackingButton = findViewById(R.id.startTrackingButton);
        stopTrackingButton = findViewById(R.id.stopTrackingButton);
        busSpinner = findViewById(R.id.busSpinner);
        routeSpinner = findViewById(R.id.routeSpinner);

        apiService = RetrofitClient.getApiService();

        setupInitialSpinners();

        IntentFilter filter =
                new IntentFilter("TRANSITPULSE_LOCATION_UPDATE");

        ContextCompat.registerReceiver(
                this,
                locationReceiver,
                filter,
                ContextCompat.RECEIVER_NOT_EXPORTED
        );

        // Load actual backend records and UUIDs.
        loadBuses();
        loadRoutes();

        startTrackingButton.setOnClickListener(v -> startTrip());

        stopTrackingButton.setOnClickListener(v -> endTrip());

        stopTrackingButton.setEnabled(false);
    }

    private void setupInitialSpinners() {
        ArrayAdapter<String> busAdapter =
                new ArrayAdapter<>(
                        this,
                        android.R.layout.simple_spinner_item,
                        new String[]{"Loading buses..."}
                );

        busAdapter.setDropDownViewResource(
                android.R.layout.simple_spinner_dropdown_item
        );
        busSpinner.setAdapter(busAdapter);

        ArrayAdapter<String> routeAdapter =
                new ArrayAdapter<>(
                        this,
                        android.R.layout.simple_spinner_item,
                        new String[]{"Loading routes..."}
                );

        routeAdapter.setDropDownViewResource(
                android.R.layout.simple_spinner_dropdown_item
        );
        routeSpinner.setAdapter(routeAdapter);
    }

    private void loadBuses() {
        apiService.getBuses().enqueue(new Callback<JsonElement>() {
            @Override
            public void onResponse(
                    Call<JsonElement> call,
                    Response<JsonElement> response) {

                if (!response.isSuccessful() || response.body() == null) {
                    showMessage("Unable to load buses. HTTP " +
                            response.code());
                    return;
                }

                JsonArray records = extractArray(response.body());
                if (records == null) {
                    showMessage("Unexpected buses response format.");
                    return;
                }

                List<String> labels = new ArrayList<>();
                busIds.clear();
                labels.add("Select Bus");
                busIds.add("");

                for (JsonElement element : records) {
                    if (!element.isJsonObject()) continue;

                    JsonObject bus = element.getAsJsonObject();
                    String id = readString(bus, "id");
                    String number = readString(bus, "bus_number");

                    if (!id.isEmpty() && !number.isEmpty()) {
                        busIds.add(id);
                        labels.add(number);
                    }
                }

                setSpinnerItems(busSpinner, labels);

                if (busIds.size() == 1) {
                    showMessage("No valid buses were returned by the backend.");
                }
            }

            @Override
            public void onFailure(Call<JsonElement> call, Throwable t) {
                showMessage("Could not load buses: " + t.getMessage());
            }
        });
    }

    private void loadRoutes() {
        apiService.getRoutes().enqueue(new Callback<JsonElement>() {
            @Override
            public void onResponse(
                    Call<JsonElement> call,
                    Response<JsonElement> response) {

                if (!response.isSuccessful() || response.body() == null) {
                    showMessage("Unable to load routes. HTTP " +
                            response.code());
                    return;
                }

                JsonArray records = extractArray(response.body());
                if (records == null) {
                    showMessage("Unexpected routes response format.");
                    return;
                }

                List<String> labels = new ArrayList<>();
                routeIds.clear();
                labels.add("Select Route");
                routeIds.add("");

                for (JsonElement element : records) {
                    if (!element.isJsonObject()) continue;

                    JsonObject route = element.getAsJsonObject();
                    String id = readString(route, "id");
                    String code = readString(route, "route_code");
                    String name = readString(route, "name");

                    String label = !code.isEmpty()
                            ? code + (name.isEmpty() ? "" : ": " + name)
                            : name;

                    if (!id.isEmpty() && !label.isEmpty()) {
                        routeIds.add(id);
                        labels.add(label);
                    }
                }

                setSpinnerItems(routeSpinner, labels);

                if (routeIds.size() == 1) {
                    showMessage("No valid routes were returned by the backend.");
                }
            }

            @Override
            public void onFailure(Call<JsonElement> call, Throwable t) {
                showMessage("Could not load routes: " + t.getMessage());
            }
        });
    }

    private JsonArray extractArray(JsonElement body) {
        if (body == null || body.isJsonNull()) return null;

        if (body.isJsonArray()) {
            return body.getAsJsonArray();
        }

        if (body.isJsonObject()) {
            JsonObject object = body.getAsJsonObject();

            // Also support common wrapped API responses.
            String[] possibleKeys = {"items", "results", "data"};

            for (String key : possibleKeys) {
                if (object.has(key) && object.get(key).isJsonArray()) {
                    return object.getAsJsonArray(key);
                }
            }
        }

        return null;
    }

    private String readString(JsonObject object, String key) {
        if (object.has(key)
                && !object.get(key).isJsonNull()
                && object.get(key).isJsonPrimitive()) {
            return object.get(key).getAsString();
        }

        return "";
    }

    private void setSpinnerItems(
            Spinner spinner,
            List<String> items) {

        ArrayAdapter<String> adapter =
                new ArrayAdapter<>(
                        this,
                        android.R.layout.simple_spinner_item,
                        items
                );

        adapter.setDropDownViewResource(
                android.R.layout.simple_spinner_dropdown_item
        );
        spinner.setAdapter(adapter);
    }

    private void startTrip() {
        if (tripRequestInProgress || tripId != null) {
            showMessage("A trip is already active or starting.");
            return;
        }

        int busPosition = busSpinner.getSelectedItemPosition();
        int routePosition = routeSpinner.getSelectedItemPosition();

        if (busPosition <= 0 || busPosition >= busIds.size()) {
            showMessage("Please select a valid bus.");
            return;
        }

        if (routePosition <= 0 || routePosition >= routeIds.size()) {
            showMessage("Please select a valid route.");
            return;
        }

        if (!hasLocationPermission()) {
            ActivityCompat.requestPermissions(
                    this,
                    new String[]{
                            Manifest.permission.ACCESS_FINE_LOCATION,
                            Manifest.permission.ACCESS_COARSE_LOCATION
                    },
                    LOCATION_PERMISSION_REQUEST_CODE
            );
            return;
        }

        String busUuid = busIds.get(busPosition);
        String routeUuid = routeIds.get(routePosition);

        tripRequestInProgress = true;
        startTrackingButton.setEnabled(false);
        showMessage("Creating trip with backend...");

        StartTripRequest request =
                new StartTripRequest(busUuid, routeUuid);

        apiService.createTrip(request).enqueue(new Callback<TripResponse>() {
            @Override
            public void onResponse(
                    Call<TripResponse> call,
                    Response<TripResponse> response) {

                tripRequestInProgress = false;

                if (!response.isSuccessful()
                        || response.body() == null
                        || response.body().getTripId() == null
                        || response.body().getTripId().trim().isEmpty()) {

                    startTrackingButton.setEnabled(true);
                    showMessage("Trip creation failed. HTTP " +
                            response.code());
                    return;
                }

                TripResponse result = response.body();
                String status = result.getStatus();

                if (status == null || !"ACTIVE".equalsIgnoreCase(status)) {
                    startTrackingButton.setEnabled(true);
                    showMessage("Backend did not confirm an ACTIVE trip.");
                    return;
                }

                // Official ID comes only from the backend.
                tripId = result.getTripId();

                journeyText.setText(
                        "Trip Started\n\n" +
                                "Trip ID: " + tripId +
                                "\nBus: " + busSpinner.getSelectedItem() +
                                "\nRoute: " + routeSpinner.getSelectedItem() +
                                "\nStatus: " + status
                );

                stopTrackingButton.setEnabled(true);

                // Start GPS only after backend confirms trip creation.
                startLocationService();
            }

            @Override
            public void onFailure(Call<TripResponse> call, Throwable t) {
                tripRequestInProgress = false;
                startTrackingButton.setEnabled(true);
                showMessage("Could not create trip: " + t.getMessage());
            }
        });
    }

    private void endTrip() {
        if (tripId == null || endRequestInProgress) {
            showMessage("There is no active trip to end.");
            return;
        }

        endRequestInProgress = true;
        stopTrackingButton.setEnabled(false);
        showMessage("Ending trip with backend...");

        String activeTripId = tripId;

        apiService.endTrip(activeTripId).enqueue(new Callback<JsonElement>() {
            @Override
            public void onResponse(
                    Call<JsonElement> call,
                    Response<JsonElement> response) {

                endRequestInProgress = false;

                if (!response.isSuccessful()) {
                    stopTrackingButton.setEnabled(true);
                    showMessage("Could not end trip. HTTP " +
                            response.code());
                    return;
                }

                // Stop GPS only after backend accepts the end request.
                stopLocationService();

                tripId = null;
                startTrackingButton.setEnabled(true);

                journeyText.setText(
                        "Trip Completed\n\n" +
                                "Trip ID: " + activeTripId +
                                "\nStatus: COMPLETED"
                );

                locationText.setText("Tracking stopped.");
            }

            @Override
            public void onFailure(Call<JsonElement> call, Throwable t) {
                endRequestInProgress = false;
                stopTrackingButton.setEnabled(true);
                showMessage("Could not contact backend to end trip: " +
                        t.getMessage());
            }
        });
    }

    private boolean hasLocationPermission() {
        return ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_FINE_LOCATION
        ) == PackageManager.PERMISSION_GRANTED
                || ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_COARSE_LOCATION
        ) == PackageManager.PERMISSION_GRANTED;
    }

    private void startLocationService() {
        if (!hasLocationPermission()) {
            showMessage("Location permission is required to start tracking.");
            return;
        }


        Intent serviceIntent =
                new Intent(this, LocationService.class);

// Pass the Trip ID received from the backend.
        serviceIntent.putExtra(
                LocationService.EXTRA_TRIP_ID,
                tripId
        );

        ContextCompat.startForegroundService(this, serviceIntent);
        locationText.setText("Starting GPS tracking...");
    }

    private void stopLocationService() {
        Intent serviceIntent =
                new Intent(this, LocationService.class);

        stopService(serviceIntent);
        locationText.setText("Tracking stopped.");
    }

    private void showMessage(String message) {
        locationText.setText(message);
    }

    @Override
    public void onRequestPermissionsResult(
            int requestCode,
            String[] permissions,
            int[] grantResults) {

        super.onRequestPermissionsResult(
                requestCode,
                permissions,
                grantResults
        );

        if (requestCode == LOCATION_PERMISSION_REQUEST_CODE) {
            if (hasLocationPermission()) {
                showMessage(
                        "Location permission granted. Press Start Journey again."
                );
            } else {
                showMessage("Location permission denied.");
            }
        }
    }

    @Override
    protected void onDestroy() {
        unregisterReceiver(locationReceiver);
        super.onDestroy();
    }
}

