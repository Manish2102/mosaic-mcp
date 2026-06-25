import os
import pyodbc

SQL_SERVER            = os.getenv("SQL_SERVER")
SQL_DATABASE          = os.getenv("SQL_DATABASE")
SQL_CONNECTION_STRING = os.getenv("SQL_CONNECTION_STRING")


def get_connection() -> pyodbc.Connection:
    if SQL_CONNECTION_STRING:
        return pyodbc.connect(SQL_CONNECTION_STRING)

    if not SQL_SERVER or not SQL_DATABASE:
        raise ValueError(
            "Set SQL_SERVER and SQL_DATABASE env vars for Managed Identity, "
            "or SQL_CONNECTION_STRING for local."
        )

    conn_str = (
        f"Driver={{ODBC Driver 18 for SQL Server}};"
        f"Server={SQL_SERVER};"
        f"Database={SQL_DATABASE};"
        f"Authentication=ActiveDirectoryMsi;"
    )
    return pyodbc.connect(conn_str)


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
