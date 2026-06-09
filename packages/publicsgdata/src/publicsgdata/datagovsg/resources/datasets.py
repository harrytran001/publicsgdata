from __future__ import annotations

import json
import time
from collections.abc import AsyncIterator, Iterator, Mapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any
from urllib.parse import urlparse

from publicsgdata._pagination import AsyncCkanSearchIterator, CkanSearchIterator, SyncPageIterator
from publicsgdata.datagovsg._request import DataGovSGHost
from publicsgdata.datagovsg.models import (
    DatasetListResponse,
    DatasetMetadata,
    DatasetRow,
    DatasetRowsResponse,
    DatastoreSearchResult,
    DownloadFilter,
    DownloadInitiateResponse,
    DownloadPollResponse,
)
from publicsgdata.datagovsg.resources._downloads import build_download_body

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

    def initiate_download(
        self,
        dataset_id: str,
        *,
        column_names: Sequence[str] | None = None,
        filters: Sequence[DownloadFilter | Mapping[str, Any]] | None = None,
    ) -> DownloadInitiateResponse:
        path = f"/datasets/{dataset_id}/initiate-download"
        payload = self._client._request_json(
            "GET",
            DataGovSGHost.DOWNLOAD,
            path,
            json=build_download_body(column_names=column_names, filters=filters),
        )
        return DownloadInitiateResponse.model_validate(self._client._catalog_data(payload))

    def poll_download(
        self,
        dataset_id: str,
        *,
        column_names: Sequence[str] | None = None,
        filters: Sequence[DownloadFilter | Mapping[str, Any]] | None = None,
    ) -> DownloadPollResponse:
        path = f"/datasets/{dataset_id}/poll-download"
        payload = self._client._request_json(
            "GET",
            DataGovSGHost.DOWNLOAD,
            path,
            json=build_download_body(column_names=column_names, filters=filters),
        )
        return DownloadPollResponse.model_validate(self._client._catalog_data(payload))

    def get_download_url(
        self,
        dataset_id: str,
        *,
        column_names: Sequence[str] | None = None,
        filters: Sequence[DownloadFilter | Mapping[str, Any]] | None = None,
        skip_initiate: bool = False,
        poll_interval: float = 2.0,
        timeout: float = 300.0,
    ) -> str:
        if not skip_initiate:
            self.initiate_download(
                dataset_id, column_names=column_names, filters=filters
            )

        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            result = self.poll_download(
                dataset_id, column_names=column_names, filters=filters
            )
            if result.url:
                return result.url
            time.sleep(poll_interval)

        raise TimeoutError(
            f"Timed out waiting for download URL for dataset {dataset_id!r}"
        )

    def download_file(
        self,
        dataset_id: str,
        destination: str | Path,
        *,
        column_names: Sequence[str] | None = None,
        filters: Sequence[DownloadFilter | Mapping[str, Any]] | None = None,
        skip_initiate: bool = False,
        poll_interval: float = 2.0,
        timeout: float = 300.0,
    ) -> Path:
        url = self.get_download_url(
            dataset_id,
            column_names=column_names,
            filters=filters,
            skip_initiate=skip_initiate,
            poll_interval=poll_interval,
            timeout=timeout,
        )
        response = self._client._http_client.get(url)
        response.raise_for_status()

        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(response.content)
        return path

    @staticmethod
    def _guess_filename(url: str, dataset_id: str) -> str:
        parsed = urlparse(url)
        name = Path(parsed.path).name
        return name or f"{dataset_id}.csv"


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

    async def initiate_download(
        self,
        dataset_id: str,
        *,
        column_names: Sequence[str] | None = None,
        filters: Sequence[DownloadFilter | Mapping[str, Any]] | None = None,
    ) -> DownloadInitiateResponse:
        path = f"/datasets/{dataset_id}/initiate-download"
        payload = await self._client._request_json(
            "GET",
            DataGovSGHost.DOWNLOAD,
            path,
            json=build_download_body(column_names=column_names, filters=filters),
        )
        return DownloadInitiateResponse.model_validate(self._client._catalog_data(payload))

    async def poll_download(
        self,
        dataset_id: str,
        *,
        column_names: Sequence[str] | None = None,
        filters: Sequence[DownloadFilter | Mapping[str, Any]] | None = None,
    ) -> DownloadPollResponse:
        path = f"/datasets/{dataset_id}/poll-download"
        payload = await self._client._request_json(
            "GET",
            DataGovSGHost.DOWNLOAD,
            path,
            json=build_download_body(column_names=column_names, filters=filters),
        )
        return DownloadPollResponse.model_validate(self._client._catalog_data(payload))

    async def get_download_url(
        self,
        dataset_id: str,
        *,
        column_names: Sequence[str] | None = None,
        filters: Sequence[DownloadFilter | Mapping[str, Any]] | None = None,
        skip_initiate: bool = False,
        poll_interval: float = 2.0,
        timeout: float = 300.0,
    ) -> str:
        import asyncio

        if not skip_initiate:
            await self.initiate_download(
                dataset_id, column_names=column_names, filters=filters
            )

        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            result = await self.poll_download(
                dataset_id, column_names=column_names, filters=filters
            )
            if result.url:
                return result.url
            await asyncio.sleep(poll_interval)

        raise TimeoutError(
            f"Timed out waiting for download URL for dataset {dataset_id!r}"
        )

    async def download_file(
        self,
        dataset_id: str,
        destination: str | Path,
        *,
        column_names: Sequence[str] | None = None,
        filters: Sequence[DownloadFilter | Mapping[str, Any]] | None = None,
        skip_initiate: bool = False,
        poll_interval: float = 2.0,
        timeout: float = 300.0,
    ) -> Path:
        url = await self.get_download_url(
            dataset_id,
            column_names=column_names,
            filters=filters,
            skip_initiate=skip_initiate,
            poll_interval=poll_interval,
            timeout=timeout,
        )
        response = await self._client._http_client.get(url)
        response.raise_for_status()

        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(response.content)
        return path
