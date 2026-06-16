import os
import pyodbc
from tools.mcp_instance import mcp

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_CONNECTION_STRING = os.getenv("SQL_CONNECTION_STRING")


def get_connection():
    """Connect via Managed Identity on Azure, or connection string locally."""
    if SQL_CONNECTION_STRING:
        return pyodbc.connect(SQL_CONNECTION_STRING)

    if not SQL_SERVER or not SQL_DATABASE:
        raise ValueError("Set SQL_SERVER and SQL_DATABASE env vars for Managed Identity, or SQL_CONNECTION_STRING for local.")

    conn_str = (
        f"Driver={{ODBC Driver 18 for SQL Server}};"
        f"Server={SQL_SERVER};"
        f"Database={SQL_DATABASE};"
        f"Authentication=ActiveDirectoryMsi;"
    )
    return pyodbc.connect(conn_str)


@mcp.tool()
def query_database(sql: str) -> str:
    """Execute a SQL query against Azure SQL and return results as a formatted table."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return "Query returned no results."

        result = " | ".join(columns) + "\n"
        result += "-" * len(result) + "\n"
        for row in rows:
            result += " | ".join(str(val) for val in row) + "\n"

        return result
    except Exception as e:
        return f"Error executing query: {str(e)}"
