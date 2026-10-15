
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
