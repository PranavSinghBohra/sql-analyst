from typing import TypedDict, Optional


class SQLAnalystState(TypedDict):
    question: str
    schema_context: str
    allowed_tables: list[str]
    sql_query: str
    error: Optional[str]
    retry_count: int
    rows: Optional[list[dict]]
    chart_spec: Optional[dict]
    final_message: Optional[str]
    insight: Optional[str]