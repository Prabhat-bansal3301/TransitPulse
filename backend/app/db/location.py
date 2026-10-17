
from datetime import datetime
from uuid import UUID

from psycopg.rows import dict_row

from app.db.connection import get_connection


def create_location(
    trip_id: UUID,
    latitude: float,
    longitude: float,
    recorded_at: datetime,
    speed: float | None = None,
):
    connection = get_connection()

    try:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT id
                FROM trips
                WHERE id = %s AND status = 'ACTIVE'
                FOR UPDATE;
                """,
                (trip_id,),
            )

            trip = cursor.fetchone()

            if trip is None:
                connection.rollback()
                return None

            cursor.execute(
                """
                INSERT INTO locations (
                    trip_id, latitude, longitude, location,
                    speed, recorded_at, received_at
                )
                VALUES (
                    %s, %s, %s,
                    ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
                    %s, %s, NOW()
                )
                RETURNING id, trip_id, latitude, longitude,
                          speed, recorded_at, received_at;
                """,
                (
                    trip_id,
                    latitude,
                    longitude,
                    longitude,
                    latitude,
                    speed,
                    recorded_at,
                ),
            )

            location = cursor.fetchone()

        connection.commit()
        return location

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_latest_location_for_bus(bus_id: UUID):
    connection = get_connection()

    try:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT
                    l.id AS location_id,
                    t.bus_id,
                    l.trip_id,
                    l.latitude,
                    l.longitude,
                    l.speed,
                    l.recorded_at,
                    l.received_at
                FROM trips t
                JOIN locations l ON l.trip_id = t.id
                WHERE t.bus_id = %s
                  AND t.status = 'ACTIVE'
                ORDER BY l.recorded_at DESC, l.received_at DESC
                LIMIT 1;
                """,
                (bus_id,),
            )

            return cursor.fetchone()

    finally:
        connection.close()
