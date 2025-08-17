# macro-indicators

Python client for the **Macroeconomy Indicators API** (World Bank data).  

- **No dependencies** beyond `requests`
- **Function-based API**
- **Annual data** (2000–present)
- **10 key macroeconomic indicators** (GDP, inflation, unemployment, M2, debt-to-GDP, etc.)
- **Country coverage**: ~180 countries with available World Bank data
- **Data source**: [World Bank Open Data](https://data.worldbank.org/)
- **Updates**: monthly snapshots

---

## Installation

```bash
pip install macro-indicators
```

---

## Quick usage

```python
from macro_indicators import root, get_country_codes, get_country_data

print(root())
# {"message": "Welcome to the Macroeconomy Indicators API"}

codes = get_country_codes()
print("Sample:", codes[:5])

data = get_country_data("SWE", "M2_LCU", 2010, 2015)
print("Years:", data["years"])
print("Values:", data["values"])
```

---

## Error handling

This client raises typed exceptions and forwards the server’s detail messages:

- `BadRequest (400)`: invalid parameter bounds (e.g. years out of range)
- `NotFound (404)`: missing country or indicator
- `MacroAPIError`: other HTTP/network errors

---

## API reference

- `root() -> dict`
- `get_country_codes() -> list[str]`
- `get_countries_with_names() -> dict[str, str]`
- `get_indicators() -> list[dict]`
- `get_country_data(country_code: str, indicator: str, start_year: int, end_year: int) -> dict`
