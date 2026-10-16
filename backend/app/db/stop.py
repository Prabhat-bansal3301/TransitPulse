
from psycopg.rows import dict_row

from app.db.connection import get_connection


def get_all_stops():
    connection = get_connection()

    try:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                SELECT
                    id,
                    name,
                    latitude,
                    longitude,
                    is_active,
                    created_at
                FROM stops
                ORDER BY name;
            """)

            return cursor.fetchall()

    finally:
        connection.close()


def create_stop(name: str, latitude: float, longitude: float):
    connection = get_connection()

    try:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                INSERT INTO stops (
                    name,
                    latitude,
                    longitude,
                    location
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    ST_SetSRID(
                        ST_MakePoint(%s, %s),
                        4326
                    )::geography
                )
                RETURNING
                    id,
                    name,
                    latitude,
                    longitude,
                    is_active,
                    created_at;
            """, (
                name,
                latitude,
                longitude,
                longitude,
                latitude,
            ))

            stop = cursor.fetchone()

        connection.commit()
        return stop

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
