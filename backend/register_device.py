from uuid import UUID
import hashlib
import secrets
import sys

from app.db.connection import get_connection


def register_device(device_identifier: str, bus_id: str | None = None):
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO devices (
                    device_identifier,
                    device_token_hash,
                    bus_id
                )
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (device_identifier, token_hash, bus_id),
            )
            device_id = cursor.fetchone()[0]

        connection.commit()

        print(f"Device ID: {device_id}")
        print(f"Device identifier: {device_identifier}")
        print(f"Device token (save it securely; shown only once): {token}")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print(
            "Usage: python register_device.py "
            "<device_identifier> [bus_id]"
        )
        raise SystemExit(1)

    identifier = sys.argv[1]
    assigned_bus_id = UUID(sys.argv[2]) if len(sys.argv) == 3 else None

    register_device(identifier, assigned_bus_id)
