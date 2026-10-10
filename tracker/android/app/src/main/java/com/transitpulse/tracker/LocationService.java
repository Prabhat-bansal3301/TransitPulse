package com.transitpulse.tracker;

import android.Manifest;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Location;
import android.os.Build;
import android.os.IBinder;

import androidx.annotation.Nullable;
import androidx.core.app.ActivityCompat;
import androidx.core.app.NotificationCompat;

import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationCallback;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationResult;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.location.Priority;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
import java.util.TimeZone;

public class LocationService extends Service {

    public static final String ACTION_LOCATION_UPDATE =
            "TRANSITPULSE_LOCATION_UPDATE";

    public static final String EXTRA_LATITUDE = "latitude";
    public static final String EXTRA_TRIP_ID = "trip_id";
    public static final String EXTRA_LONGITUDE = "longitude";
    public static final String EXTRA_ACCURACY = "accuracy";
    public static final String EXTRA_SPEED = "speed";
    public static final String EXTRA_RECORDED_AT = "recorded_at";

    private static final String CHANNEL_ID = "transitpulse_location_channel";
    private static final int NOTIFICATION_ID = 101;

    // Collect GPS measurements approximately every 5 seconds.
    private static final long LOCATION_INTERVAL_MS = 5000L;

    private FusedLocationProviderClient fusedLocationClient;
    private LocationCallback locationCallback;

    @Override
    public void onCreate() {
        super.onCreate();

        fusedLocationClient =
                LocationServices.getFusedLocationProviderClient(this);

        createNotificationChannel();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {

        startForeground(NOTIFICATION_ID, buildNotification());

        startLocationUpdates();

        // Service may be recreated by Android; it does not create a Trip ID.
        return START_STICKY;
    }

    private void startLocationUpdates() {

        if (ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_FINE_LOCATION
        ) != PackageManager.PERMISSION_GRANTED
                && ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_COARSE_LOCATION
        ) != PackageManager.PERMISSION_GRANTED) {

            stopSelf();
            return;
        }

        LocationRequest locationRequest =
                new LocationRequest.Builder(
                        Priority.PRIORITY_HIGH_ACCURACY,
                        LOCATION_INTERVAL_MS
                )
                        .setMinUpdateIntervalMillis(LOCATION_INTERVAL_MS)
                        .build();

        locationCallback = new LocationCallback() {
            @Override
            public void onLocationResult(LocationResult locationResult) {

                if (locationResult == null) {
                    return;
                }

                for (Location location : locationResult.getLocations()) {
                    broadcastLocation(location);
                }
            }
        };

        fusedLocationClient.requestLocationUpdates(
                locationRequest,
                locationCallback,
                getMainLooper()
        );
    }

    private void broadcastLocation(Location location) {

        // Android returns speed in meters per second (m/s).
// Convert m/s to kilometers per hour (km/h).
        double speedMps = location.hasSpeed() ? location.getSpeed() : 0.0;
        double speedKmh = speedMps * 3.6;

        Intent intent = new Intent(ACTION_LOCATION_UPDATE);
        intent.setPackage(getPackageName());

        intent.putExtra(EXTRA_LATITUDE, location.getLatitude());
        intent.putExtra(EXTRA_LONGITUDE, location.getLongitude());
        intent.putExtra(EXTRA_ACCURACY, location.getAccuracy());

        // The existing MainActivity reads the "speed" extra.
        // Its value is now km/s, not m/s.
        intent.putExtra(EXTRA_SPEED, (float) speedKmh);

        // Timestamp when this GPS measurement was recorded.
        intent.putExtra(EXTRA_RECORDED_AT, formatRecordedAt(location));

        sendBroadcast(intent);
    }

    private String formatRecordedAt(Location location) {

        long recordedTimeMillis = location.getTime();

        // Use current UTC time only if the location has no usable timestamp.
        if (recordedTimeMillis <= 0) {
            recordedTimeMillis = System.currentTimeMillis();
        }

        SimpleDateFormat formatter = new SimpleDateFormat(
                "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'",
                Locale.US
        );

        formatter.setTimeZone(TimeZone.getTimeZone("UTC"));

        return formatter.format(new Date(recordedTimeMillis));
    }

    private Notification buildNotification() {

        Intent openAppIntent = new Intent(this, MainActivity.class);

        int pendingIntentFlags = PendingIntent.FLAG_UPDATE_CURRENT;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            pendingIntentFlags |= PendingIntent.FLAG_IMMUTABLE;
        }

        PendingIntent pendingIntent = PendingIntent.getActivity(
                this,
                0,
                openAppIntent,
                pendingIntentFlags
        );

        return new NotificationCompat.Builder(this, CHANNEL_ID)
                .setContentTitle("TransitPulse GPS Tracking")
                .setContentText("Collecting location measurements")
                .setSmallIcon(android.R.drawable.ic_menu_mylocation)
                .setContentIntent(pendingIntent)
                .setOngoing(true)
                .build();
    }

    private void createNotificationChannel() {

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {

            NotificationChannel channel = new NotificationChannel(
                    CHANNEL_ID,
                    "TransitPulse Location Tracking",
                    NotificationManager.IMPORTANCE_LOW
            );

            channel.setDescription(
                    "Notification for active bus location tracking"
            );

            NotificationManager manager =
                    getSystemService(NotificationManager.class);

            if (manager != null) {
                manager.createNotificationChannel(channel);
            }
        }
    }

    @Override
    public void onDestroy() {

        if (fusedLocationClient != null && locationCallback != null) {
            fusedLocationClient.removeLocationUpdates(locationCallback);
        }

        super.onDestroy();
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}

