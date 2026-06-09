from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import httpx

from publicsgdata._constants import DEFAULT_TIMEOUT, default_api_key
from publicsgdata.datagovsg._request import DataGovSGHost, DataGovSGRequestMixin
from publicsgdata.datagovsg.resources.collections import CollectionsResource
from publicsgdata.datagovsg.resources.datasets import DatasetsResource
from publicsgdata.datagovsg.resources.realtime import RealtimeResource


class DataGovSGClient(DataGovSGRequestMixin):
    """Sync client for data.gov.sg APIs."""

    _http_client: httpx.Client

    def __init__(
        self,
        *,
        api_key: str | None = None,
        http_client: httpx.Client | None = None,
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
            self._http_client = httpx.Client(timeout=timeout)
            self._owns_client = True

        self.collections = CollectionsResource(self)
        self.datasets = DatasetsResource(self)
        self.realtime = RealtimeResource(self)

    def __enter__(self) -> DataGovSGClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_client:
            self._http_client.close()

    def _request_json(
        self,
        method: str,
        host: DataGovSGHost,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = self._build_url(host, path)
        encoded = self._encode_query(params) if params else None
        response = self._http_client.request(
            method,
            url,
            params=encoded,
            headers=self._merge_headers(),
        )
        payload = self._parse_json(response)
        if not isinstance(payload, dict):
            self._raise_for_response(response, payload=payload)
            return {}
        self._raise_for_response(response, payload=payload)
        return payload
