from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, cast

import httpx

from publicsgdata._constants import DEFAULT_TIMEOUT, HEADER_API_KEY
from publicsgdata._exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
)


class BaseHTTPClient:
    """Shared HTTP helpers for sync and async clients."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = 0,
    ) -> None:
        self._api_key = api_key
        self._timeout = timeout
        self._max_retries = max_retries
        self._owns_client = False

    def _auth_headers(self) -> dict[str, str]:
        if self._api_key:
            return {HEADER_API_KEY: self._api_key}
        return {}

    def _merge_headers(self, headers: Mapping[str, str] | None = None) -> dict[str, str]:
        merged = dict(self._auth_headers())
        if headers:
            merged.update(headers)
        return merged

    def _parse_json(self, response: httpx.Response) -> Any:
        if not response.content:
            return None
        return response.json()

    def _raise_for_response(
        self,
        response: httpx.Response,
        *,
        payload: Any | None = None,
    ) -> None:
        if response.is_success:
            if isinstance(payload, dict):
                code = payload.get("code")
                if code not in (None, 0) and payload.get("success") is not True:
                    self._raise_api_payload(response, payload)
            return

        data = payload if payload is not None else self._parse_json(response)
        if response.status_code == 429:
            raise RateLimitError(
                _error_message(data, response),
                status_code=429,
                code=_error_code(data),
                name=_error_name(data),
                body=data,
            )
        if response.status_code in (401, 403):
            raise AuthenticationError(
                _error_message(data, response),
                status_code=response.status_code,
                code=_error_code(data),
                name=_error_name(data),
                body=data,
            )
        if response.status_code == 404:
            raise NotFoundError(
                _error_message(data, response),
                status_code=404,
                code=_error_code(data),
                name=_error_name(data),
                body=data,
            )
        raise APIError(
            _error_message(data, response),
            status_code=response.status_code,
            code=_error_code(data),
            name=_error_name(data),
            body=data,
        )

    def _raise_api_payload(self, response: httpx.Response, payload: dict[str, Any]) -> None:
        message = _error_message(payload, response)
        code = _error_code(payload)
        name = _error_name(payload)
        if response.status_code == 429 or code == 429:
            raise RateLimitError(message, status_code=429, code=code, name=name, body=payload)
        if name and "NOT_FOUND" in name.upper():
            raise NotFoundError(message, status_code=404, code=code, name=name, body=payload)
        raise APIError(
            message,
            status_code=response.status_code,
            code=code,
            name=name,
            body=payload,
        )


def _error_message(data: Any, response: httpx.Response) -> str:
    if isinstance(data, dict):
        for key in ("errorMsg", "message", "error"):
            value = data.get(key)
            if isinstance(value, str) and value:
                return value
            if isinstance(value, dict):
                return str(value)
        if data.get("success") is False and isinstance(data.get("error"), dict):
            return str(data["error"])
    return f"HTTP {response.status_code} error for {response.request.url}"


def _error_code(data: Any) -> int | str | None:
    if isinstance(data, dict) and "code" in data:
        return cast(int | str | None, data.get("code"))
    return None


def _error_name(data: Any) -> str | None:
    if isinstance(data, dict) and isinstance(data.get("name"), str):
        return cast(str, data["name"])
    return None


SyncHTTPClient = httpx.Client
AsyncHTTPClient = httpx.AsyncClient
HTTPMethod = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
