__version__ = "0.0.1"
__author__ = "Pantarbengt"

from .api import (
    root,
    get_country_codes,
    get_countries_with_names,
    get_indicators,
    get_country_data,
    MacroAPIError,
    BadRequest,
    NotFound,
)

__all__ = [
    "root",
    "get_country_codes",
    "get_countries_with_names",
    "get_indicators",
    "get_country_data",
    "MacroAPIError",
    "BadRequest",
    "NotFound",
]
