from decimal import Decimal

import pandas as pd


def _to_jsonable(value):
    if isinstance(value, Decimal):
        return float(value)
    return value


def build_chart_spec(rows: list[dict]) -> dict:
    if not rows:
        return {"type": "empty", "x": None, "y": None, "data": []}

    clean_rows = [{k: _to_jsonable(v) for k, v in row.items()} for row in rows]
    df = pd.DataFrame(clean_rows)

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    non_numeric_cols = [c for c in df.columns if c not in numeric_cols]

    if len(df.columns) == 2 and len(numeric_cols) == 1 and len(non_numeric_cols) == 1:
        chart_type = "bar"
        x, y = non_numeric_cols[0], numeric_cols[0]
    elif any("date" in c.lower() for c in df.columns) and numeric_cols:
        chart_type = "line"
        x = next(c for c in df.columns if "date" in c.lower())
        y = numeric_cols[0]
    else:
        chart_type = "table"
        x = y = None

    return {"type": chart_type, "x": x, "y": y, "data": clean_rows}