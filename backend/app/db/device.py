
import hashlib

from psycopg.rows import dict_row

from app.db.connection import get_connection


def get_active_device_by_token(token: str):
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()

    connection = get_connection()

    try:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT id, device_identifier, bus_id, is_active
                FROM devices
                WHERE device_token_hash = %s
                  AND is_active = TRUE;
                """,
                (token_hash,),
            )

            return cursor.fetchone()

    finally:
        connection.close()
