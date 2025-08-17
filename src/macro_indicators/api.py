from __future__ import annotations
from typing import Dict, List, Any, Optional
import requests

_BASE_URL = "https://macro-indicators.fly.dev"
_TIMEOUT = 30


# ---------- Exceptions ----------
class MacroAPIError(RuntimeError):
    """Base error for macro-indicators client."""
    def __init__(self, message: str, *, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class BadRequest(MacroAPIError):
    """400: Invalid parameters (e.g., years out of bounds)."""


class NotFound(MacroAPIError):
    """404: Country or indicator not found."""


# ---------- Internal helpers ----------
def _extract_detail(resp: requests.Response) -> str:
    """Try to extract FastAPI's {"detail": "..."}; fall back to response text."""
    ctype = resp.headers.get("content-type", "")
    if "application/json" in ctype:
        try:
            js = resp.json()
            if isinstance(js, dict) and "detail" in js:
                return str(js["detail"])
        except Exception:
            pass
    return (resp.text or "").strip() or f"HTTP {resp.status_code}"


def _get(path: str, *, params: Optional[Dict[str, Any]] = None) -> Any:
    """GET wrapper with normalized error handling.

    Raises:
        BadRequest: on 400 (with API `detail` as message).
        NotFound: on 404 (with API `detail` as message).
        MacroAPIError: on other HTTP/network errors.
    """
    url = f"{_BASE_URL}{path}"
    try:
        resp = requests.get(url, params=params, timeout=_TIMEOUT)
    except requests.RequestException as e:
        raise MacroAPIError(f"Network error calling {url}: {e}") from e

    if resp.status_code == 400:
        raise BadRequest(_extract_detail(resp), status_code=400)
    if resp.status_code == 404:
        raise NotFound(_extract_detail(resp), status_code=404)

    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        raise MacroAPIError(_extract_detail(resp), status_code=resp.status_code) from e

    if resp.headers.get("content-type", "").startswith("application/json"):
        return resp.json()
    return {"raw": resp.text}


# ---------- Public functions ----------
def root() -> Dict[str, str]:
    """
    Fetch a welcome message from the API root endpoint.

    Returns:
        dict: {"message": "Welcome to the Macroeconomy Indicators API"}

    Example:
        >>> from macro_indicators import root
        >>> root()
        {"message": "Welcome to the Macroeconomy Indicators API"}
    """
    return _get("/")


def get_country_codes() -> List[str]:
    """
    Get all available country codes (ISO Alpha-3).

    Returns:
        list[str]

    Example:
        >>> from macro_indicators import get_country_codes
        >>> get_country_codes()[:5]
        ["AFG", "ALB", "DZA", "AND", "AGO", "..."]
    """
    return _get("/country-codes")


def get_countries_with_names() -> Dict[str, str]:
    """
    Get all available country codes mapped to their full names.

    Returns:
        dict[str, str]

    Example:
        >>> from macro_indicators import get_countries_with_names
        >>> d = get_countries_with_names(); list(d.items())[:3]
        [["AFG", "Afghanistan"], ["ALB", "Albania"], ["DZA", "Algeria"]]
    """
    return _get("/countries")


def get_indicators() -> List[Dict[str, Any]]:
    """
    Get all available indicators.

    Returns:
        list[dict]: Each element contains:
            - name (str)
            - code (str)
            - description (str)
            - unit (str)

    Example:
        >>> from macro_indicators import get_indicators
        >>> inds = get_indicators(); inds[0]
        {"name": "M2_LCU", "code": "FM.LBL.BMNY.CN", "description": "Broad money (M2), current local currency units", "unit": "LCU"}
    """
    return _get("/indicators")


def get_country_data(country_code: str, indicator: str, start_year: int, end_year: int) -> Dict[str, Any]:
    """
    Fetch indicator data for a given country.

    Args:
        country_code (str): ISO Alpha-3 country code (e.g. "SWE").
        indicator (str): Indicator name (e.g. "M2_LCU").
        start_year (int): Start year (>= 2000).
        end_year (int): End year (<= current year).

    Returns:
        dict: Keys:
            - country (str)
            - country_name (str)
            - indicator (str)
            - description (str)
            - unit (str)
            - years (list[int])
            - values (list[float | None])

    Raises:
        NotFound: if country or indicator does not exist.
        BadRequest: for invalid years or parameter validation failures.

    Example:
        >>> from macro_indicators import get_country_data
        >>> resp = get_country_data("SWE", "M2_LCU", 2010, 2015)
        >>> resp["country_name"], resp["indicator"]
        ("Sweden", "M2_LCU")
        >>> resp["years"][:6]
        [2010, 2011, 2012, 2013, 2014, 2015]
        >>> resp["values"][:6]
        [2209655000000.0, 2356567000000.0, 2435958000000.0, 2528914000000.0, 2634557000000.0, 2809711000000.0]
    """
    return _get(
        "/data",
        params={
            "country_code": country_code,
            "indicator": indicator,
            "start_year": start_year,
            "end_year": end_year,
        },
    )
