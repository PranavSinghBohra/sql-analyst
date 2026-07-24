import psycopg2
import psycopg2.extras

from app.config import settings


def get_readonly_connection():
    return psycopg2.connect(
        host=settings.PG_HOST,
        port=settings.PG_PORT,
        dbname=settings.PG_DB,
        user=settings.PG_USER,
        password=settings.PG_PASSWORD,
        cursor_factory=psycopg2.extras.RealDictCursor,
    )


def get_table_names() -> list[str]:
    conn = get_readonly_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        )
        rows = cur.fetchall()
    conn.close()
    return [r["table_name"] for r in rows]