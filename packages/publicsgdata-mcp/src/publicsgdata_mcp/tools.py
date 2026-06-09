from __future__ import annotations

import json
from typing import Any

from publicsgdata import DataGovSGClient
from publicsgdata_mcp.cache import dataset_cache_path

MAX_PREVIEW_ROWS = 50
MAX_SEARCH_ROWS = 50

_client: DataGovSGClient | None = None


def get_client() -> DataGovSGClient:
    global _client
    if _client is None:
        _client = DataGovSGClient()
    return _client


def close_client() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None


def _json(data: Any) -> str:
    if hasattr(data, "model_dump"):
        return json.dumps(data.model_dump(), default=str)
    return json.dumps(data, default=str)


def list_datasets(page: int | None = None) -> str:
    response = get_client().datasets.list(page=page)
    return _json(response)


def get_dataset_metadata(dataset_id: str) -> str:
    metadata = get_client().datasets.get_metadata(dataset_id)
    return _json(metadata)


def preview_dataset_rows(
    dataset_id: str,
    *,
    limit: int = 10,
    cursor: str | None = None,
) -> str:
    bounded_limit = min(max(limit, 1), MAX_PREVIEW_ROWS)
    rows = get_client().datasets.list_rows(dataset_id, limit=bounded_limit, cursor=cursor)
    return _json(rows)


def search_dataset_rows(
    dataset_id: str,
    *,
    q: str | None = None,
    filters: dict[str, Any] | None = None,
    sort: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> str:
    bounded_limit = min(max(limit, 1), MAX_SEARCH_ROWS)
    result = get_client().datasets.search(
        dataset_id,
        q=q,
        filters=filters,
        sort=sort,
        limit=bounded_limit,
        offset=offset,
    )
    return _json(result)


def get_dataset_download_url(
    dataset_id: str,
    *,
    skip_initiate: bool = False,
) -> str:
    url = get_client().datasets.get_download_url(dataset_id, skip_initiate=skip_initiate)
    return _json({"dataset_id": dataset_id, "url": url})


def download_dataset_file(
    dataset_id: str,
    *,
    filename: str | None = None,
    skip_initiate: bool = False,
) -> str:
    destination = dataset_cache_path(dataset_id, filename=filename)
    path = get_client().datasets.download_file(
        dataset_id,
        destination,
        skip_initiate=skip_initiate,
    )
    metadata = get_client().datasets.get_metadata(dataset_id)
    return _json(
        {
            "dataset_id": dataset_id,
            "local_path": str(path),
            "name": metadata.name,
            "format": metadata.format,
        }
    )


def get_pm25(date: str | None = None) -> str:
    pm25 = get_client().realtime.pm25.get(date=date)
    return _json(pm25)
