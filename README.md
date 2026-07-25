# SQL Analyst

Ask questions about a database in plain English and get back a query, the result, and a chart. Built with LangGraph.

If the generated SQL fails (bad column name, wrong join, invalid table reference), it catches the error, rewrites the query, and tries again — up to 3 times before giving up.


## Architecture
```
generate_sql -> validate_and_execute
    -> error -> reflect -> validate_and_execute (retry, max 3)
    -> ok    -> generate_chart -> generate_insight -> done
```


Table schemas are stored as embeddings in Chroma so only the relevant tables get pulled into the prompt instead of dumping the whole schema every time.

Before any SQL actually runs, it goes through a guardrail built with sqlglot that parses the query and rejects anything that isn't a single read-only SELECT on a known table. Added guardrail tests to verify that only safe, read-only SQL queries are executed. for this (`backend/tests/`) and it identified a security gap early on — queries with no table reference at all (like `SELECT pg_sleep(10)`) were slipping through since the check only looked at referenced tables. Fixed by requiring at least one valid table reference.

On top of that, the app connects to Postgres through a role that only has SELECT privileges, so even if something got past the guardrail it physically can't write anything.

## Stack

LangGraph, FastAPI, Postgres, sqlglot, OpenAI API, React, Tailwind, Plotly

## Running it

Backend:
```bash
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env   # add your OpenAI key + a postgres password
python -m app.database.seed
uvicorn app.main:app --reload --port 8000
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

Then just ask something like "what is the total revenue by category".