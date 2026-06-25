from tools.mcp_instance import mcp
from services.worldbank_service import get_economic_data, compare_countries, INDICATORS


def _format_value(label: str, value) -> str:
    if value is None:
        return f"  {label}: N/A"
    if "USD" in label:
        if value >= 1_000_000_000_000:
            return f"  {label}: ${value / 1_000_000_000_000:.2f}T"
        if value >= 1_000_000_000:
            return f"  {label}: ${value / 1_000_000_000:.2f}B"
        return f"  {label}: ${value:,.0f}"
    if "Population" in label:
        return f"  {label}: {value:,.0f}"
    return f"  {label}: {value:.2f}%"


@mcp.tool()
def get_country_economic_snapshot(country_code: str) -> str:
    """
    Get a full economic snapshot of a country using World Bank data.
    Includes GDP, growth rate, inflation, unemployment, FDI and more.

    Args:
        country_code: ISO 2-letter country code e.g. US, GB, DE, IN, SG
    """
    try:
        data = get_economic_data(country_code)
    except Exception as e:
        return f"Error fetching data for '{country_code}': {e}"

    info = data.get("country", {})
    indicators = data.get("indicators", {})

    if not info.get("name"):
        return f"Country code '{country_code}' not found. Use ISO 2-letter codes e.g. US, GB, DE, IN."

    lines = [
        f"Economic Snapshot: {info.get('name')}",
        f"  Region       : {info.get('region', 'N/A')}",
        f"  Income Level : {info.get('income_level', 'N/A')}",
        f"  Capital      : {info.get('capital', 'N/A')}",
        "",
        "Key Indicators (latest available year):",
    ]
    for label, value in indicators.items():
        lines.append(_format_value(label, value))

    lines.append("")
    lines.append("Source: World Bank Open Data (api.worldbank.org)")
    return "\n".join(lines)


@mcp.tool()
def compare_country_indicator(countries: str, indicator: str = "gdp") -> str:
    """
    Compare a specific economic indicator across multiple countries.

    Args:
        countries: Comma-separated ISO 2-letter country codes e.g. US,GB,DE,IN
        indicator: One of: gdp, gdp_growth, gdp_per_capita, inflation,
                   unemployment, population, fdi
    """
    country_list = [c.strip() for c in countries.split(",") if c.strip()]
    if not country_list:
        return "Please provide at least one country code."

    available = ", ".join(INDICATORS.keys())
    try:
        data = compare_countries(country_list, indicator.lower())
    except ValueError as e:
        return f"{e}\nAvailable indicators: {available}"
    except Exception as e:
        return f"Error fetching data: {e}"

    label = data["indicator"]
    lines = [f"Comparison: {label}\n"]

    sorted_countries = sorted(
        data["countries"].items(),
        key=lambda x: x[1] if x[1] is not None else -1,
        reverse=True,
    )

    for rank, (name, value) in enumerate(sorted_countries, 1):
        formatted = _format_value(label, value).strip()
        lines.append(f"  {rank}. {name}: {formatted.split(': ', 1)[-1]}")

    lines.append("")
    lines.append("Source: World Bank Open Data (api.worldbank.org)")
    return "\n".join(lines)
