
from uuid import UUID

from psycopg.rows import dict_row

from app.db.connection import get_connection


def create_trip(bus_id: UUID, route_id: UUID):
    connection = get_connection()

    try:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                INSERT INTO trips (bus_id, route_id, status, started_at)
                VALUES (%s, %s, 'ACTIVE', NOW())
                RETURNING id, bus_id, route_id, device_id,
                          conductor_id, status, started_at,
                          completed_at, created_at;
                """,
                (bus_id, route_id),
            )
            trip = cursor.fetchone()

        connection.commit()
        return trip

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()



def get_trip_by_id(trip_id: UUID):
    connection = get_connection()

    try:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT id, bus_id, route_id, device_id,
                       conductor_id, status, started_at,
                       completed_at, created_at
                FROM trips
                WHERE id = %s;
                """,
                (trip_id,),
            )
            return cursor.fetchone()

    finally:
        connection.close()


def get_active_trips():
    connection = get_connection()

    try:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT id, bus_id, route_id, device_id,
                       conductor_id, status, started_at,
                       completed_at, created_at
                FROM trips
                WHERE status = 'ACTIVE'
                ORDER BY started_at DESC;
                """
            )
            return cursor.fetchall()

    finally:
        connection.close()



def end_trip(trip_id: UUID):
    connection = get_connection()

    try:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                UPDATE trips
                SET status = 'COMPLETED',
                    completed_at = NOW()
                WHERE id = %s
                  AND status = 'ACTIVE'
                RETURNING id, bus_id, route_id, device_id,
                          conductor_id, status, started_at,
                          completed_at, created_at;
                """,
                (trip_id,),
            )
            trip = cursor.fetchone()

        connection.commit()
        return trip

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
