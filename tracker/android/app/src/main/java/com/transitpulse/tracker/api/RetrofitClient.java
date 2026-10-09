package com.transitpulse.tracker.api;


import okhttp3.Interceptor;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

import java.io.IOException;

public class RetrofitClient {

    // Android Emulator -> computer localhost, port 8000.
    private static final String BASE_URL =
            "http://10.0.2.2:8000/";

    private static Retrofit retrofit;

    // Leave empty until Developer 2 confirms the authentication contract.
    private static String authToken = "";

    private RetrofitClient() {
        // Prevent creating instances of this utility class.
    }

    public static synchronized Retrofit getClient() {

        if (retrofit == null) {

            OkHttpClient client = new OkHttpClient.Builder()
                    .addInterceptor(new Interceptor() {
                        @Override
                        public Response intercept(Chain chain)
                                throws IOException {

                            Request original = chain.request();

                            Request.Builder requestBuilder =
                                    original.newBuilder()
                                            .header(
                                                    "Accept",
                                                    "application/json"
                                            );

                            String token = authToken;

                            // Add Bearer authentication only when a token
                            // is configured and the backend uses this scheme.
                            if (token != null && !token.trim().isEmpty()) {
                                requestBuilder.header(
                                        "Authorization",
                                        "Bearer " + token
                                );
                            }

                            return chain.proceed(
                                    requestBuilder.build()
                            );
                        }
                    })
                    .build();

            retrofit = new Retrofit.Builder()
                    .baseUrl(BASE_URL)
                    .client(client)
                    .addConverterFactory(
                            GsonConverterFactory.create()
                    )
                    .build();
        }

        return retrofit;
    }

    public static ApiService getApiService() {
        return getClient().create(ApiService.class);
    }

    // Call this after obtaining a token through the agreed authentication
    // flow. This method does not itself authenticate a device.
    public static synchronized void setAuthToken(String token) {
        authToken = token == null ? "" : token.trim();

        // Rebuild so subsequent requests use the updated token.
        retrofit = null;
    }
}

