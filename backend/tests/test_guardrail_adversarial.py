from app.guardrails.validators import validate_sql, SQLValidationError

ALLOWED = ["customers", "products", "orders", "order_items"]

ATTACKS = [
    ("Direct DROP", "DROP TABLE customers"),
    ("Direct DELETE", "DELETE FROM customers"),
    ("Direct UPDATE", "UPDATE customers SET name = 'x'"),
    ("Stacked statement", "SELECT * FROM customers; DROP TABLE customers"),
    ("Data-modifying CTE", "WITH d AS (DELETE FROM customers RETURNING *) SELECT * FROM d"),
    ("Unknown table", "SELECT * FROM pg_shadow"),
    ("Table-less function call (DoS attempt)", "SELECT pg_sleep(10)"),
    ("File read attempt", "SELECT pg_read_file('/etc/passwd')"),
    ("Case-varied DROP", "dRoP tAbLe customers"),
]

SAFE = [
    ("Normal aggregation", "SELECT category, SUM(price) FROM products GROUP BY category"),
    ("Normal join", "SELECT c.name FROM customers c JOIN orders o ON c.customer_id = o.customer_id"),
]

def run():
    print("--- Attacks (should ALL be blocked) ---")
    for name, sql in ATTACKS:
        try:
            validate_sql(sql, ALLOWED)
            print(f"[FAIL - NOT BLOCKED] {name}")
        except SQLValidationError as e:
            print(f"[PASS - blocked] {name}: {e}")

    print("\n--- Safe queries (should ALL pass) ---")
    for name, sql in SAFE:
        try:
            validate_sql(sql, ALLOWED)
            print(f"[PASS - allowed] {name}")
        except SQLValidationError as e:
            print(f"[FAIL - WRONGLY BLOCKED] {name}: {e}")

if __name__ == "__main__":
    run()