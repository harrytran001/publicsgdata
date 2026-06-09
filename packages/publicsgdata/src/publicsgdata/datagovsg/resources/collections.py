from __future__ import annotations

from typing import TYPE_CHECKING

from publicsgdata.datagovsg._request import DataGovSGHost
from publicsgdata.datagovsg.models import (
    CollectionListResponse,
    CollectionMetadata,
    CollectionMetadataResponse,
)

if TYPE_CHECKING:
    from publicsgdata.datagovsg.client import DataGovSGClient


class CollectionsResource:
    def __init__(self, client: DataGovSGClient) -> None:
        self._client = client

    def list(self) -> CollectionListResponse:
        payload = self._client._request_json("GET", DataGovSGHost.CATALOG, "/collections")
        return CollectionListResponse.model_validate(self._client._catalog_data(payload))

    def get_metadata(self, collection_id: str) -> CollectionMetadata:
        path = f"/collections/{collection_id}/metadata"
        payload = self._client._request_json("GET", DataGovSGHost.CATALOG, path)
        response = CollectionMetadataResponse.model_validate(self._client._catalog_data(payload))
        return response.collection_metadata


class AsyncCollectionsResource:
    def __init__(self, client: object) -> None:
        self._client = client

    async def list(self) -> CollectionListResponse:
        payload = await self._client._request_json("GET", DataGovSGHost.CATALOG, "/collections")  # type: ignore[attr-defined]
        return CollectionListResponse.model_validate(self._client._catalog_data(payload))  # type: ignore[attr-defined]

    async def get_metadata(self, collection_id: str) -> CollectionMetadata:
        path = f"/collections/{collection_id}/metadata"
        payload = await self._client._request_json("GET", DataGovSGHost.CATALOG, path)  # type: ignore[attr-defined]
        response = CollectionMetadataResponse.model_validate(self._client._catalog_data(payload))  # type: ignore[attr-defined]
        return response.collection_metadata
