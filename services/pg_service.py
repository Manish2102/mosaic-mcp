import os
import psycopg2

PG_HOST     = os.getenv("PGHOST",     "mosaic-poc.postgres.database.azure.com")
PG_PORT     = int(os.getenv("PGPORT", "5432"))
PG_DATABASE = os.getenv("PGDATABASE", "postgres")
PG_USER     = os.getenv("PGUSER",     "mosaic")
PG_PASSWORD = os.getenv("PGPASSWORD", "")


def get_connection() -> psycopg2.extensions.connection:
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
        sslmode="require",
    )


def execute_query(sql: str) -> dict:
    """
    Execute a SQL statement.
    Returns {"columns": [...], "rows": [...]} for SELECT,
    or {"rows_affected": n} for INSERT/UPDATE/DELETE.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)

        if cursor.description:
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            return {"columns": columns, "rows": rows}

        affected = cursor.rowcount
        conn.commit()
        return {"rows_affected": affected}
    finally:
        conn.close()
