from app.agents.sql_generator import llm


def generate_insight(question: str, rows: list[dict]) -> str:
    if not rows:
        return "The query ran successfully but returned no rows."

    preview = rows[:20]
    prompt = (
        f"Question: {question}\n\n"
        f"Query result (first {len(preview)} rows):\n{preview}\n\n"
        "Write a 1-2 sentence plain-English summary of what this shows. "
        "Mention specific numbers where relevant. No preamble."
    )
    response = llm.invoke(prompt)
    return response.content