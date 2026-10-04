from app.db.connection import get_connection


def get_all_buses():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, bus_number, operator, is_active, created_at
                FROM buses
                ORDER BY bus_number;
            """)

            return cursor.fetchall()

    finally:
        connection.close()