
from uuid import UUID

from psycopg.rows import dict_row

from app.db.connection import get_connection


def get_all_buses():
    connection = get_connection()

    try:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                SELECT
                    b.id,
                    b.bus_number,
                    b.operator,
                    b.depot_id,
                    d.depot_name,
                    b.is_active,
                    b.created_at
                FROM buses b
                LEFT JOIN depots d ON b.depot_id = d.id
                ORDER BY b.bus_number;
            """)

            return cursor.fetchall()

    finally:
        connection.close()


def get_bus_by_id(bus_id: UUID):
    connection = get_connection()

    try:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                SELECT
                    b.id,
                    b.bus_number,
                    b.operator,
                    b.depot_id,
                    d.depot_name,
                    b.is_active,
                    b.created_at
                FROM buses b
                LEFT JOIN depots d ON b.depot_id = d.id
                WHERE b.id = %s;
            """, (bus_id,))

            return cursor.fetchone()

    finally:
        connection.close()

def create_bus(bus_number: str, operator: str | None, depot_id: UUID | None):
    connection = get_connection()

    try:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                INSERT INTO buses (bus_number, operator, depot_id)
                VALUES (%s, %s, %s)
                RETURNING id, bus_number, operator, depot_id,
                          is_active, created_at;
            """, (bus_number, operator, depot_id))

            bus = cursor.fetchone()

            cursor.execute("""
                SELECT depot_name
                FROM depots
                WHERE id = %s;
            """, (depot_id,))

            depot = cursor.fetchone()
            bus["depot_name"] = depot["depot_name"] if depot else None

        connection.commit()
        return bus

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
