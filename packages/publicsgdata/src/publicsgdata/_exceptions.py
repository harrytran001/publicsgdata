from __future__ import annotations

from typing import Any


class PublicSGDataError(Exception):
    """Base exception for publicsgdata."""


class APIError(PublicSGDataError):
    """Raised when the API returns an error response."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        code: int | str | None = None,
        name: str | None = None,
        body: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.name = name
        self.body = body


class RateLimitError(APIError):
    """Raised when rate limits are exceeded (HTTP 429)."""


class AuthenticationError(APIError):
    """Raised when authentication fails (HTTP 401/403)."""


class NotFoundError(APIError):
    """Raised when a resource is not found (HTTP 404)."""
