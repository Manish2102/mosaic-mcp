from .mcp_instance import mcp
from . import add_tools   # noqa: F401 - registers add, greet tools
from . import sql_tools   # noqa: F401 - registers query_database tool
from . import uuid_tools  # noqa: F401 - registers generate_uuid tool
from . import user_tools   # noqa: F401 - registers get_user_info tool
from . import market_tools # noqa: F401 - registers get_country_economic_snapshot, compare_country_indicator
from . import pg_tools     # noqa: F401 - registers query_postgres tool
