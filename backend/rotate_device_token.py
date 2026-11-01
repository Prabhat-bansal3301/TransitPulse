
import hashlib
import secrets
from uuid import UUID

from app.db.connection import get_connection

DEVICE_ID = UUID("2fef822d-c2f1-4bbf-8be1-caaaf7ae1c99")


def rotate_device_token():
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE devices
                SET device_token_hash = %s
                WHERE id = %s
                  AND is_active = TRUE
                RETURNING id;
                """,
                (token_hash, DEVICE_ID),
            )

            device = cursor.fetchone()

            if device is None:
                connection.rollback()
                raise RuntimeError(
                    "Active device not found; token was not rotated."
                )

        connection.commit()
        print("Device token rotated successfully.")
        print("New token (save securely; shown only once):")
        print(token)

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    rotate_device_token()
