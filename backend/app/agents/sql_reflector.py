from app.agents.sql_generator import SQLQuery, generator


def reflect_and_rewrite(question: str, schema_context: str, failed_sql: str, error: str) -> str:
    prompt = (
        f"Relevant schema:\n{schema_context}\n\n"
        f"Question: {question}\n\n"
        f"This SQL failed:\n{failed_sql}\n\n"
        f"Error:\n{error}\n\n"
        "Diagnose the problem and write a corrected single read-only "
        "Postgres SELECT statement."
    )
    result: SQLQuery = generator.invoke(prompt)
    return result.sql