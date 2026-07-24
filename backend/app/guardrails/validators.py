import sqlglot
from sqlglot import exp

FORBIDDEN_NODE_TYPES = (
    exp.Insert,
    exp.Update,
    exp.Delete,
    exp.Drop,
    exp.Alter,
    exp.Create,
    exp.TruncateTable,
)


class SQLValidationError(Exception):
    pass


def validate_sql(sql: str, allowed_tables: list[str], default_limit: int = 1000) -> str:
    sql = sql.strip().rstrip(";")

    try:
        parsed = sqlglot.parse(sql, read="postgres")
    except sqlglot.errors.ParseError as e:
        raise SQLValidationError(f"Could not parse SQL: {e}")

    parsed = [s for s in parsed if s is not None]
    if len(parsed) != 1:
        raise SQLValidationError("Only a single SELECT statement is allowed.")

    statement = parsed[0]

    if not isinstance(statement, exp.Select):
        raise SQLValidationError(
            f"Only SELECT statements are allowed, got {type(statement).__name__}."
        )

    for node in statement.walk():
        if isinstance(node[0], FORBIDDEN_NODE_TYPES):
            raise SQLValidationError(f"Forbidden operation: {type(node[0]).__name__}")

    referenced = {t.name.lower() for t in statement.find_all(exp.Table)}
    allowed_lower = {t.lower() for t in allowed_tables}

    if not referenced:
        raise SQLValidationError("Query must reference at least one known table.")
    
    unknown = referenced - allowed_lower

    if unknown:
        raise SQLValidationError(f"Query references unknown table(s): {unknown}")

    if not statement.find(exp.Limit):
        statement = statement.limit(default_limit)

    return statement.sql(dialect="postgres")