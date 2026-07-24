import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # LLM
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Postgres (read-only app connection)
    PG_HOST = os.getenv("PG_HOST", "localhost")
    PG_PORT = os.getenv("PG_PORT", "5432")
    PG_DB = os.getenv("PG_DB", "shop")
    PG_USER = os.getenv("PG_USER", "sql_analyst_app")
    PG_PASSWORD = os.getenv("PG_PASSWORD", "change-me")

    PG_ADMIN_USER = os.getenv("PG_ADMIN_USER", "postgres")
    PG_ADMIN_PASSWORD = os.getenv("PG_ADMIN_PASSWORD", "")

    CHECKPOINT_DB_PATH = os.getenv("CHECKPOINT_DB_PATH", "./checkpoints.sqlite")

    # Guardrail
    DEFAULT_QUERY_LIMIT = int(os.getenv("DEFAULT_QUERY_LIMIT", "1000"))
    MAX_SQL_RETRIES = int(os.getenv("MAX_SQL_RETRIES", "3"))


settings = Settings()