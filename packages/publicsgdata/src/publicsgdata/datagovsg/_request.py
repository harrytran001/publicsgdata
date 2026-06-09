from __future__ import annotations

from collections.abc import Mapping
from enum import Enum
from typing import Any
from urllib.parse import urljoin

from publicsgdata._base_client import BaseHTTPClient
from publicsgdata._constants import CATALOG_BASE_URL, CKAN_BASE_URL, REALTIME_BASE_URL


class DataGovSGHost(str, Enum):
    CATALOG = "catalog"
    CKAN = "ckan"
    REALTIME = "realtime"


class DataGovSGRequestMixin(BaseHTTPClient):
    """HTTP request helpers routed to data.gov.sg hosts."""

    def _base_url(self, host: DataGovSGHost) -> str:
        if host is DataGovSGHost.CATALOG:
            return CATALOG_BASE_URL
        if host is DataGovSGHost.CKAN:
            return CKAN_BASE_URL
        return REALTIME_BASE_URL

    def _build_url(self, host: DataGovSGHost, path: str) -> str:
        base = self._base_url(host)
        if not path.startswith("/"):
            path = f"/{path}"
        return urljoin(f"{base}/", path.lstrip("/"))

    def _catalog_data(self, payload: dict[str, Any]) -> dict[str, Any]:
        data = payload.get("data")
        if isinstance(data, dict):
            return data
        return payload

    def _realtime_data(self, payload: dict[str, Any]) -> dict[str, Any]:
        data = payload.get("data")
        if isinstance(data, dict):
            return data
        return payload

    @staticmethod
    def _cursor_params(cursor: str | None, *, limit: int | None = None) -> dict[str, str]:
        params: dict[str, str] = {}
        if limit is not None:
            params["limit"] = str(limit)
        if cursor:
            for part in cursor.split("&"):
                if "=" in part:
                    key, value = part.split("=", 1)
                    params[key] = value
        return params

    @staticmethod
    def _encode_query(params: Mapping[str, Any]) -> dict[str, str]:
        encoded: dict[str, str] = {}
        for key, value in params.items():
            if value is None:
                continue
            encoded[key] = str(value)
        return encoded
