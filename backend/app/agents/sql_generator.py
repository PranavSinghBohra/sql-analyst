from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from app.config import settings
from app.database.schema_retrieval import retrieve_schema_context


class SQLQuery(BaseModel):
    sql: str = Field(description="A single read-only Postgres SELECT statement, no markdown fences.")

def generate_sql(question: str) -> dict:
    schema_context, allowed_tables = retrieve_schema_context(question)

    prompt = (
        f"Relevant schema:\n{schema_context}\n\n"
        f"Question: {question}\n\n"
        "Write a single read-only Postgres SELECT statement that answers it. "
        "Only use the tables and columns shown above."
    )
    result: SQLQuery = generator.invoke(prompt)

    return {
        "sql_query": result.sql,
        "schema_context": schema_context,
        "allowed_tables": allowed_tables,
    }

llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=settings.OPENAI_API_KEY)
generator = llm.with_structured_output(SQLQuery)