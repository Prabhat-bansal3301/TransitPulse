
from uuid import UUID
from psycopg.rows import dict_row
from app.db.connection import get_connection

def get_all_routes():
    connection = get_connection()

    try:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                SELECT
                    id,
                    route_code,
                    name,
                    description,
                    is_active,
                    created_at
                FROM routes
                ORDER BY route_code;
            """)

            return cursor.fetchall()

    finally:
        connection.close()


def create_route(route_code: str, name: str, description: str | None):
    connection = get_connection()

    try:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                INSERT INTO routes (route_code, name, description)
                VALUES (%s, %s, %s)
                RETURNING id, route_code, name, description,
                          is_active, created_at;
            """, (route_code, name, description))

            route = cursor.fetchone()

        connection.commit()
        return route

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_route_by_id(route_id: UUID):
    connection = get_connection()

    try:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                SELECT
                    id,
                    route_code,
                    name,
                    description,
                    is_active,
                    created_at
                FROM routes
                WHERE id = %s;
            """, (route_id,))

            return cursor.fetchone()

    finally:
        connection.close()


def add_stop_to_route(
    route_id: UUID,
    stop_id: UUID,
    stop_sequence: int,
):
    connection = get_connection()

    try:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                INSERT INTO route_stops (
                    route_id,
                    stop_id,
                    stop_sequence
                )
                VALUES (%s, %s, %s)
                RETURNING
                    id,
                    route_id,
                    stop_id,
                    stop_sequence,
                    created_at;
            """, (route_id, stop_id, stop_sequence))

            route_stop = cursor.fetchone()

        connection.commit()
        return route_stop

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()



def get_stops_for_route(route_id: UUID):
    connection = get_connection()

    try:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                SELECT
                    s.id,
                    s.name,
                    s.latitude,
                    s.longitude,
                    rs.stop_sequence
                FROM route_stops rs
                JOIN stops s ON s.id = rs.stop_id
                WHERE rs.route_id = %s
                  AND s.is_active = TRUE
                ORDER BY rs.stop_sequence;
            """, (route_id,))

            return cursor.fetchall()

    finally:
        connection.close()
