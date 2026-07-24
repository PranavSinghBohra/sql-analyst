from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

from app.config import settings
from app.graph.state import SQLAnalystState
from app.agents.sql_generator import generate_sql
from app.agents.sql_reflector import reflect_and_rewrite
from app.services.sql_service import run_query
from app.services.chart_service import build_chart_spec

import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

from app.agents.insight_generator import generate_insight



MAX_RETRIES = settings.MAX_SQL_RETRIES


def generate_sql_node(state: SQLAnalystState) -> dict:
    result = generate_sql(state["question"])
    return {**result, "error": None}


def validate_and_execute_node(state: SQLAnalystState) -> dict:
    result = run_query(state["sql_query"], state["allowed_tables"])
    if result["error"]:
        return {"error": result["error"], "sql_query": result["sql"]}
    return {"rows": result["rows"], "sql_query": result["sql"], "error": None}


def reflect_node(state: SQLAnalystState) -> dict:
    new_sql = reflect_and_rewrite(
        question=state["question"],
        schema_context=state["schema_context"],
        failed_sql=state["sql_query"],
        error=state["error"],
    )
    return {"sql_query": new_sql, "retry_count": state.get("retry_count", 0) + 1, "error": None}


def generate_chart_node(state: SQLAnalystState) -> dict:
    chart_spec = build_chart_spec(state["rows"])
    return {"chart_spec": chart_spec, "final_message": None}


def give_up_node(state: SQLAnalystState) -> dict:
    return {"final_message": f"Failed after {MAX_RETRIES} attempts. Last error: {state['error']}"}


def generate_insight_node(state: SQLAnalystState) -> dict:
    insight = generate_insight(state["question"], state["rows"])
    return {"insight": insight}


def route_after_execution(state: SQLAnalystState) -> str:
    if state.get("error"):
        if state.get("retry_count", 0) >= MAX_RETRIES:
            return "give_up"
        return "reflect"
    return "generate_chart"


def build_graph():
    builder = StateGraph(SQLAnalystState)

    builder.add_node("generate_sql", generate_sql_node)
    builder.add_node("validate_and_execute", validate_and_execute_node)
    builder.add_node("reflect", reflect_node)
    builder.add_node("generate_chart", generate_chart_node)
    builder.add_node("generate_insight", generate_insight_node)
    builder.add_node("give_up", give_up_node)

    builder.set_entry_point("generate_sql")
    builder.add_edge("generate_sql", "validate_and_execute")
    builder.add_conditional_edges(
        "validate_and_execute",
        route_after_execution,
        {"reflect": "reflect", "generate_chart": "generate_chart", "give_up": "give_up"},
    )
    builder.add_edge("reflect", "validate_and_execute")
    builder.add_edge("generate_chart", "generate_insight")
    builder.add_edge("generate_insight", END)
    builder.add_edge("give_up", END)

    conn = sqlite3.connect(settings.CHECKPOINT_DB_PATH, check_same_thread=False)
    memory = SqliteSaver(conn)
    return builder.compile(checkpointer=memory)