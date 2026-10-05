from uuid import UUID

from psycopg.rows import dict_row

from app.db.connection import get_connection


def get_all_buses():
    connection = get_connection()

    try:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                SELECT id, bus_number, operator, is_active, created_at
                FROM buses
                ORDER BY bus_number;
            """)

            return cursor.fetchall()

    finally:
        connection.close()


def get_bus_by_id(bus_id: UUID):
    connection = get_connection()

    try:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                SELECT id, bus_number, operator, is_active, created_at
                FROM buses
                WHERE id = %s;
            """, (bus_id,))

            return cursor.fetchone()

    finally:
        connection.close()