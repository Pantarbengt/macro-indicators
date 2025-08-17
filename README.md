# macro-indicators

A tiny Python client for the **Macroeconomy Indicators API** running on Fly.io.

- **No dependencies** beyond `requests`  
- **Function-based API** (no classes)  
- **Clean error handling** that mirrors the server’s `detail` messages  

> Base URL: `https://macro-indicators.fly.dev`

---

## Installation

Install from PyPI:

```bash
pip install macro-indicators
```

From source (development):

```bash
git clone https://github.com/Pantarbengt/macro-indicators.git
cd macro-indicators
pip install -e .
```

---

## Get started

```python
from macro_indicators import (
    root,
    get_country_codes,
    get_countries_with_names,
    get_indicators,
    get_country_data,
)

print(root())
# {'message': 'Welcome to the Macroeconomy Indicators API'}

codes = get_country_codes()
print("Number of country codes:", len(codes), "sample:", codes[:5])

countries = get_countries_with_names()
print("SWE ->", countries.get("SWE"))

inds = get_indicators()
print("First indicator:", inds[0] if inds else None)

data = get_country_data("SWE", "M2_LCU", 2010, 2015)
print("Years:", data["years"])
print("Values:", data["values"])
```

---

## Examples

### `root()`

```python
from macro_indicators import root
root()
# {"message": "Welcome to the Macroeconomy Indicators API"}
```

### `get_country_codes()`

```python
from macro_indicators import get_country_codes
get_country_codes()[:5]
# ["AFG", "ALB", "DZA", "AND", "AGO", "..."]
```

### `get_countries_with_names()`

```python
from macro_indicators import get_countries_with_names
d = get_countries_with_names()
list(d.items())[:3]
# [["AFG", "Afghanistan"], ["ALB", "Albania"], ["DZA", "Algeria"]]
```

### `get_indicators()`

```python
from macro_indicators import get_indicators
inds = get_indicators()
inds[0]
# {"name": "M2_LCU", "code": "FM.LBL.BMNY.CN",
#  "description": "Broad money (M2), current local currency units", "unit": "LCU"}
```

### `get_country_data()`

```python
from macro_indicators import get_country_data
resp = get_country_data("SWE", "M2_LCU", 2010, 2015)
resp["country_name"], resp["indicator"]
# ("Sweden", "M2_LCU")
resp["years"]
# [2010, 2011, 2012, 2013, 2014, 2015]
resp["values"][:3]
# [2209655000000.0, 2356567000000.0, 2435958000000.0]
```

---

## Error handling

This client raises typed exceptions and forwards the server’s `detail`:

- `BadRequest` (400): invalid parameter bounds (e.g. years)  
- `NotFound` (404): missing country or indicator  
- `MacroAPIError`: other HTTP/network errors; includes `status_code` when available  

```python
from macro_indicators import get_country_data, NotFound, BadRequest

# 404: indicator not found
try:
    get_country_data("AFG", "NO_SUCH_INDICATOR", 2010, 2015)
except NotFound as e:
    print("NotFound:", e, e.status_code)

# 400: bad year range
try:
    get_country_data("SWE", "CPI", 1990, 1995)
except BadRequest as e:
    print("BadRequest:", e, e.status_code)
```

---

## API reference

- `root() -> dict`  
- `get_country_codes() -> list[str]`  
- `get_countries_with_names() -> dict[str, str]`  
- `get_indicators() -> list[dict]` (each item has `name`, `code`, `description`, `unit`)  
- `get_country_data(country_code: str, indicator: str, start_year: int, end_year: int) -> dict`  

Return from `get_country_data`:

```json
{
  "country": "SWE",
  "country_name": "Sweden",
  "indicator": "M2_LCU",
  "description": "...",
  "unit": "LCU",
  "years": [2010, 2011, ...],
  "values": [2209655000000.0, 2356567000000.0, ...]
}
```

---

## Development

```bash
# install in editable mode
pip install -e .

# quick manual tests
python - << "PY"
from macro_indicators import root, get_indicators, get_country_data
print(root())
ind = get_indicators()[0]["name"]
print("Using indicator:", ind)
print(get_country_data("SWE", ind, 2010, 2015)["years"])
PY
```

---

## License

TBD. Consider adding an OSI-approved license (MIT, Apache-2.0) before publishing to PyPI.

---

## Links

- API docs: [https://macro-indicators.fly.dev/docs](https://macro-indicators.fly.dev/docs)  
- Issues: [https://github.com/Pantarbengt/macro-indicators/issues](https://github.com/Pantarbengt/macro-indicators/issues)
