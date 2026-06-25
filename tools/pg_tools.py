from tools.mcp_instance import mcp
from services.pg_service import execute_query


@mcp.tool()
def query_postgres(sql: str) -> str:
    """
    Execute any SQL against the Bregal PostgreSQL database and return results.
    SELECT returns a formatted table. INSERT/UPDATE/DELETE returns rows affected.

    Args:
        sql: SQL statement to execute
    """
    try:
        result = execute_query(sql)

        if "rows_affected" in result:
            return f"Query executed successfully. Rows affected: {result['rows_affected']}"

        columns = result["columns"]
        rows = result["rows"]

        if not rows:
            return "Query returned no results."

        header = " | ".join(columns)
        separator = "-" * len(header)
        lines = [header, separator] + [" | ".join(str(v) for v in row) for row in rows]
        return "\n".join(lines)

    except Exception as e:
        return f"Error: {str(e)}"
