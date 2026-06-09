from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import httpx

from publicsgdata._constants import DEFAULT_TIMEOUT, default_api_key
from publicsgdata.datagovsg._request import DataGovSGHost, DataGovSGRequestMixin
from publicsgdata.datagovsg.resources.collections import AsyncCollectionsResource
from publicsgdata.datagovsg.resources.datasets import AsyncDatasetsResource
from publicsgdata.datagovsg.resources.realtime import AsyncRealtimeResource


class AsyncDataGovSGClient(DataGovSGRequestMixin):
    """Async client for data.gov.sg APIs."""

    _http_client: httpx.AsyncClient

    def __init__(
        self,
        *,
        api_key: str | None = None,
        http_client: httpx.AsyncClient | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = 0,
    ) -> None:
        super().__init__(
            api_key=api_key or default_api_key(), timeout=timeout, max_retries=max_retries
        )
        if http_client is not None:
            self._http_client = http_client
            self._owns_client = False
        else:
            self._http_client = httpx.AsyncClient(timeout=timeout)
            self._owns_client = True

        self.collections = AsyncCollectionsResource(self)
        self.datasets = AsyncDatasetsResource(self)
        self.realtime = AsyncRealtimeResource(self)

    async def __aenter__(self) -> AsyncDataGovSGClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    async def close(self) -> None:
        if self._owns_client:
            await self._http_client.aclose()

    async def _request_json(
        self,
        method: str,
        host: DataGovSGHost,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = self._build_url(host, path)
        encoded = self._encode_query(params) if params else None
        response = await self._http_client.request(
            method,
            url,
            params=encoded,
            json=json,
            headers=self._merge_headers(),
        )
        payload = self._parse_json(response)
        if not isinstance(payload, dict):
            self._raise_for_response(response, payload=payload)
            return {}
        self._raise_for_response(response, payload=payload)
        return payload
