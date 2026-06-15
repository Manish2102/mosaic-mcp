"""
This is the module docstring.
It details the file's purpose, exported classes, and key functions.
"""
import os
import pyodbc
from tools.mcp_instance import mcp

def get_connection():
    """Establish a connection to the SQL database using the connection string from environment variables."""
    conn_str = os.getenv("SQL_CONNECTION_STRING")
    if not conn_str:
        raise ValueError("SQL_CONNECTION_STRING environment variable is not set.")
    return pyodbc.connect(conn_str)


@mcp.tool()
def query_database(sql: str) -> str:
    """Execute a SQL query and return the results as a formatted string."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return "Query returned no results."

        # Format as a readable table
        result = " | ".join(columns) + "\n"
        result += "-" * len(result) + "\n"
        for row in rows:
            result += " | ".join(str(val) for val in row) + "\n"

        return result
    except Exception as e:
        return f"Error executing query: {str(e)}"
