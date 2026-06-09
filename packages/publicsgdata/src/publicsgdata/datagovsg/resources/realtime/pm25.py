from __future__ import annotations

from typing import TYPE_CHECKING

from publicsgdata.datagovsg._request import DataGovSGHost
from publicsgdata.datagovsg.models import PM25Response

if TYPE_CHECKING:
    from publicsgdata.datagovsg.async_client import AsyncDataGovSGClient
    from publicsgdata.datagovsg.client import DataGovSGClient


class PM25Resource:
    def __init__(self, client: DataGovSGClient) -> None:
        self._client = client

    def get(
        self,
        *,
        date: str | None = None,
        pagination_token: str | None = None,
    ) -> PM25Response:
        params: dict[str, str] = {}
        if date is not None:
            params["date"] = date
        if pagination_token is not None:
            params["paginationToken"] = pagination_token
        payload = self._client._request_json(
            "GET",
            DataGovSGHost.REALTIME,
            "/pm25",
            params=params or None,
        )
        return PM25Response.model_validate(self._client._realtime_data(payload))


class AsyncPM25Resource:
    def __init__(self, client: AsyncDataGovSGClient) -> None:
        self._client = client

    async def get(
        self,
        *,
        date: str | None = None,
        pagination_token: str | None = None,
    ) -> PM25Response:
        params: dict[str, str] = {}
        if date is not None:
            params["date"] = date
        if pagination_token is not None:
            params["paginationToken"] = pagination_token
        payload = await self._client._request_json(
            "GET",
            DataGovSGHost.REALTIME,
            "/pm25",
            params=params or None,
        )
        return PM25Response.model_validate(self._client._realtime_data(payload))
