from __future__ import annotations

import json
from collections.abc import AsyncIterator, Iterator, Mapping
from typing import TYPE_CHECKING, Any

from publicsgdata._pagination import AsyncCkanSearchIterator, CkanSearchIterator, SyncPageIterator
from publicsgdata.datagovsg._request import DataGovSGHost
from publicsgdata.datagovsg.models import (
    DatasetListResponse,
    DatasetMetadata,
    DatasetRow,
    DatasetRowsResponse,
    DatastoreSearchResult,
)

if TYPE_CHECKING:
    from publicsgdata.datagovsg.async_client import AsyncDataGovSGClient
    from publicsgdata.datagovsg.client import DataGovSGClient


class DatasetsResource:
    def __init__(self, client: DataGovSGClient) -> None:
        self._client = client

    def list(self, *, page: int | None = None) -> DatasetListResponse:
        params = {"page": page} if page is not None else None
        payload = self._client._request_json(
            "GET", DataGovSGHost.CATALOG, "/datasets", params=params
        )
        return DatasetListResponse.model_validate(self._client._catalog_data(payload))

    def get_metadata(self, dataset_id: str) -> DatasetMetadata:
        path = f"/datasets/{dataset_id}/metadata"
        payload = self._client._request_json("GET", DataGovSGHost.CATALOG, path)
        return DatasetMetadata.model_validate(self._client._catalog_data(payload))

    def list_rows(
        self,
        dataset_id: str,
        *,
        limit: int = 100,
        cursor: str | None = None,
    ) -> DatasetRowsResponse:
        path = f"/datasets/{dataset_id}/list-rows"
        params = self._client._cursor_params(cursor, limit=limit)
        payload = self._client._request_json("GET", DataGovSGHost.CATALOG, path, params=params)
        return DatasetRowsResponse.model_validate(self._client._catalog_data(payload))

    def iter_rows(
        self,
        dataset_id: str,
        *,
        limit: int = 100,
        cursor: str | None = None,
    ) -> Iterator[DatasetRow]:
        iterator: SyncPageIterator[DatasetRow] = SyncPageIterator(
            lambda next_cursor: self.list_rows(dataset_id, limit=limit, cursor=next_cursor),
            get_items=lambda response: response.rows,
            get_next_cursor=lambda response: (
                response.links.next if response.links is not None else None
            ),
        )
        iterator._cursor = cursor
        return iterator

    def search(
        self,
        resource_id: str,
        *,
        limit: int = 100,
        offset: int = 0,
        filters: Mapping[str, Any] | None = None,
        q: str | Mapping[str, Any] | None = None,
        sort: str | None = None,
        fields: str | None = None,
    ) -> DatastoreSearchResult:
        params: dict[str, Any] = {
            "resource_id": resource_id,
            "limit": limit,
            "offset": offset,
        }
        if filters is not None:
            params["filters"] = json.dumps(filters)
        if q is not None:
            params["q"] = json.dumps(q) if isinstance(q, Mapping) else q
        if sort is not None:
            params["sort"] = sort
        if fields is not None:
            params["fields"] = fields

        payload = self._client._request_json(
            "GET",
            DataGovSGHost.CKAN,
            "/api/action/datastore_search",
            params=params,
        )
        result = payload.get("result", payload)
        records = result.get("records", [])
        return DatastoreSearchResult(
            resource_id=result.get("resource_id", resource_id),
            fields=result.get("fields", []),
            records=records,
            total=result.get("total", len(records)),
            limit=result.get("limit", limit),
            offset=offset,
            links=result.get("_links", {}),
        )

    def iter_search(
        self,
        resource_id: str,
        *,
        limit: int = 100,
        offset: int = 0,
        filters: Mapping[str, Any] | None = None,
        q: str | Mapping[str, Any] | None = None,
        sort: str | None = None,
    ) -> Iterator[DatasetRow]:
        def fetch_page(page_offset: int) -> DatastoreSearchResult:
            return self.search(
                resource_id,
                limit=limit,
                offset=page_offset,
                filters=filters,
                q=q,
                sort=sort,
            )

        return CkanSearchIterator(fetch_page, initial_offset=offset)


class AsyncDatasetsResource:
    def __init__(self, client: AsyncDataGovSGClient) -> None:
        self._client = client

    async def list(self, *, page: int | None = None) -> DatasetListResponse:
        params = {"page": page} if page is not None else None
        payload = await self._client._request_json(
            "GET", DataGovSGHost.CATALOG, "/datasets", params=params
        )
        return DatasetListResponse.model_validate(self._client._catalog_data(payload))

    async def get_metadata(self, dataset_id: str) -> DatasetMetadata:
        path = f"/datasets/{dataset_id}/metadata"
        payload = await self._client._request_json("GET", DataGovSGHost.CATALOG, path)
        return DatasetMetadata.model_validate(self._client._catalog_data(payload))

    async def list_rows(
        self,
        dataset_id: str,
        *,
        limit: int = 100,
        cursor: str | None = None,
    ) -> DatasetRowsResponse:
        path = f"/datasets/{dataset_id}/list-rows"
        params = self._client._cursor_params(cursor, limit=limit)
        payload = await self._client._request_json(
            "GET", DataGovSGHost.CATALOG, path, params=params
        )
        return DatasetRowsResponse.model_validate(self._client._catalog_data(payload))

    async def iter_rows(
        self,
        dataset_id: str,
        *,
        limit: int = 100,
        cursor: str | None = None,
    ) -> AsyncIterator[DatasetRow]:
        from publicsgdata._pagination import AsyncPageIterator

        iterator: AsyncPageIterator[DatasetRow] = AsyncPageIterator(
            lambda next_cursor: self.list_rows(dataset_id, limit=limit, cursor=next_cursor),
            get_items=lambda response: response.rows,
            get_next_cursor=lambda response: (
                response.links.next if response.links is not None else None
            ),
        )
        iterator._cursor = cursor
        async for row in iterator:
            yield row

    async def search(
        self,
        resource_id: str,
        *,
        limit: int = 100,
        offset: int = 0,
        filters: Mapping[str, Any] | None = None,
        q: str | Mapping[str, Any] | None = None,
        sort: str | None = None,
        fields: str | None = None,
    ) -> DatastoreSearchResult:
        params: dict[str, Any] = {
            "resource_id": resource_id,
            "limit": limit,
            "offset": offset,
        }
        if filters is not None:
            params["filters"] = json.dumps(filters)
        if q is not None:
            params["q"] = json.dumps(q) if isinstance(q, Mapping) else q
        if sort is not None:
            params["sort"] = sort
        if fields is not None:
            params["fields"] = fields

        payload = await self._client._request_json(
            "GET",
            DataGovSGHost.CKAN,
            "/api/action/datastore_search",
            params=params,
        )
        result = payload.get("result", payload)
        records = result.get("records", [])
        return DatastoreSearchResult(
            resource_id=result.get("resource_id", resource_id),
            fields=result.get("fields", []),
            records=records,
            total=result.get("total", len(records)),
            limit=result.get("limit", limit),
            offset=offset,
            links=result.get("_links", {}),
        )

    async def iter_search(
        self,
        resource_id: str,
        *,
        limit: int = 100,
        offset: int = 0,
        filters: Mapping[str, Any] | None = None,
        q: str | Mapping[str, Any] | None = None,
        sort: str | None = None,
    ) -> AsyncIterator[DatasetRow]:
        iterator = AsyncCkanSearchIterator(
            lambda page_offset: self.search(
                resource_id,
                limit=limit,
                offset=page_offset,
                filters=filters,
                q=q,
                sort=sort,
            ),
            initial_offset=offset,
        )
        async for row in iterator:
            yield row
