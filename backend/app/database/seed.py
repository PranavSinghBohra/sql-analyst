import psycopg2

from app.config import settings

ADMIN_DSN = f"host=127.0.0.1 port={settings.PG_PORT} dbname={settings.PG_DB} user={settings.PG_ADMIN_USER} password={settings.PG_ADMIN_PASSWORD}"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    region TEXT NOT NULL,
    signup_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date DATE NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(order_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity INTEGER NOT NULL
);
"""

SEED_SQL = """
INSERT INTO customers (name, region, signup_date)
SELECT * FROM (VALUES
    ('John Doe', 'North', DATE '2024-01-15'),
    ('Jane Smith', 'South', DATE '2024-02-20'),
    ('Alice Johnson', 'East', DATE '2024-03-05'),
    ('Bob Wilson', 'West', DATE '2024-04-10')
) AS v(name, region, signup_date)
WHERE NOT EXISTS (SELECT 1 FROM customers);

INSERT INTO products (name, category, price)
SELECT * FROM (VALUES
    ('Wireless Mouse', 'Electronics', 25.00),
    ('Standing Desk', 'Furniture', 350.00),
    ('Notebook', 'Stationery', 4.50),
    ('Mechanical Keyboard', 'Electronics', 89.00)
) AS v(name, category, price)
WHERE NOT EXISTS (SELECT 1 FROM products);

INSERT INTO orders (customer_id, order_date, status)
SELECT * FROM (VALUES
    (1, DATE '2024-05-01', 'completed'),
    (2, DATE '2024-05-03', 'completed'),
    (1, DATE '2024-05-10', 'completed'),
    (3, DATE '2024-06-01', 'cancelled'),
    (4, DATE '2024-06-15', 'completed')
) AS v(customer_id, order_date, status)
WHERE NOT EXISTS (SELECT 1 FROM orders);

INSERT INTO order_items (order_id, product_id, quantity)
SELECT * FROM (VALUES
    (1, 1, 2), (1, 4, 1),
    (2, 2, 1),
    (3, 3, 5),
    (4, 1, 1),
    (5, 2, 1), (5, 4, 2)
) AS v(order_id, product_id, quantity)
WHERE NOT EXISTS (SELECT 1 FROM order_items);
"""

CREATE_READONLY_ROLE_SQL = f"""
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '{settings.PG_USER}') THEN
        CREATE ROLE {settings.PG_USER} WITH LOGIN PASSWORD '{settings.PG_PASSWORD}';
    END IF;
END
$$;

GRANT CONNECT ON DATABASE {settings.PG_DB} TO {settings.PG_USER};
GRANT USAGE ON SCHEMA public TO {settings.PG_USER};
GRANT SELECT ON ALL TABLES IN SCHEMA public TO {settings.PG_USER};
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO {settings.PG_USER};
"""


def run():
    conn = psycopg2.connect(ADMIN_DSN)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(SCHEMA_SQL)
        cur.execute(SEED_SQL)
        cur.execute(CREATE_READONLY_ROLE_SQL)
    conn.close()
    print("Schema created, demo data seeded, read-only role ready.")


if __name__ == "__main__":
    run()