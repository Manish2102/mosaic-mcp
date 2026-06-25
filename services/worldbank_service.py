import httpx

BASE_URL = "https://api.worldbank.org/v2"

INDICATORS = {
    "gdp":            ("NY.GDP.MKTP.CD",       "GDP (USD)"),
    "gdp_growth":     ("NY.GDP.MKTP.KD.ZG",    "GDP Growth (%)"),
    "gdp_per_capita": ("NY.GDP.PCAP.CD",        "GDP per Capita (USD)"),
    "inflation":      ("FP.CPI.TOTL.ZG",        "Inflation (%)"),
    "unemployment":   ("SL.UEM.TOTL.ZS",        "Unemployment (%)"),
    "population":     ("SP.POP.TOTL",           "Population"),
    "fdi":            ("BX.KLT.DINV.CD.WD",     "Foreign Direct Investment (USD)"),
}


def _fetch_indicator(country_code: str, indicator_id: str) -> float | None:
    url = f"{BASE_URL}/country/{country_code}/indicator/{indicator_id}"
    params = {"format": "json", "mrv": 1, "per_page": 1}
    with httpx.Client(timeout=10) as client:
        response = client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if len(data) > 1 and data[1]:
            return data[1][0].get("value")
    return None


def get_country_info(country_code: str) -> dict:
    """Fetch basic country metadata from World Bank."""
    url = f"{BASE_URL}/country/{country_code}"
    params = {"format": "json"}
    with httpx.Client(timeout=10) as client:
        response = client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if len(data) > 1 and data[1]:
            c = data[1][0]
            return {
                "name": c.get("name"),
                "region": c.get("region", {}).get("value"),
                "income_level": c.get("incomeLevel", {}).get("value"),
                "capital": c.get("capitalCity"),
            }
    return {}


def get_economic_data(country_code: str) -> dict:
    """Fetch all economic indicators for a country."""
    info = get_country_info(country_code.upper())
    results = {"country": info, "indicators": {}}

    for key, (indicator_id, label) in INDICATORS.items():
        value = _fetch_indicator(country_code.upper(), indicator_id)
        results["indicators"][label] = value

    return results


def compare_countries(country_codes: list[str], indicator_key: str) -> dict:
    """Compare a specific indicator across multiple countries."""
    if indicator_key not in INDICATORS:
        raise ValueError(f"Unknown indicator '{indicator_key}'. Choose from: {', '.join(INDICATORS.keys())}")

    indicator_id, label = INDICATORS[indicator_key]
    results = {"indicator": label, "countries": {}}

    for code in country_codes:
        info = get_country_info(code.upper())
        value = _fetch_indicator(code.upper(), indicator_id)
        name = info.get("name", code.upper())
        results["countries"][name] = value

    return results
