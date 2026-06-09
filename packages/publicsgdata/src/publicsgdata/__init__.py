"""publicsgdata: Python client for Singapore government public data."""

from publicsgdata._exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    PublicSGDataError,
    RateLimitError,
)
from publicsgdata.datagovsg.async_client import AsyncDataGovSGClient
from publicsgdata.datagovsg.client import DataGovSGClient

__all__ = [
    "APIError",
    "AsyncDataGovSGClient",
    "AuthenticationError",
    "DataGovSGClient",
    "NotFoundError",
    "PublicSGDataError",
    "RateLimitError",
]

__version__ = "0.2.0"
