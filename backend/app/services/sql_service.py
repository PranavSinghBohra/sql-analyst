import psycopg2

from app.database.db import get_readonly_connection
from app.guardrails.validators import validate_sql, SQLValidationError


def run_query(sql: str, allowed_tables: list[str]) -> dict:
    try:
        safe_sql = validate_sql(sql, allowed_tables)
    except SQLValidationError as e:
        return {"sql": sql, "error": str(e), "rows": None}

    try:
        conn = get_readonly_connection()
        with conn.cursor() as cur:
            cur.execute(safe_sql)
            rows = cur.fetchall()
        conn.close()
    except psycopg2.Error as e:
        return {"sql": safe_sql, "error": str(e), "rows": None}

    return {"sql": safe_sql, "error": None, "rows": [dict(r) for r in rows]}