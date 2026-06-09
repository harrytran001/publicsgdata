from __future__ import annotations

import json
from typing import Any

from publicsgdata import DataGovSGClient
from publicsgdata.datagovsg._request import DataGovSGHost
from publicsgdata_mcp.cache import dataset_cache_path
from publicsgdata_mcp.realtime_catalog import (
    describe_realtime_api,
    list_realtime_dataset_names,
    normalize_realtime_parameters,
    resolve_realtime_api,
)

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


def list_realtime_datasets() -> str:
    return _json(list_realtime_dataset_names())


def describe_realtime_dataset(dataset_name: str) -> str:
    return _json(describe_realtime_api(dataset_name))


def fetch_realtime_data(
    dataset_name: str,
    parameters: dict[str, Any] | None = None,
) -> str:
    api = resolve_realtime_api(dataset_name)
    params = normalize_realtime_parameters(api, parameters)
    client = get_client()

    if api.host == "v2_realtime":
        payload = client._request_json(
            "GET",
            DataGovSGHost.REALTIME,
            api.path,
            params=params or None,
        )
        data = client._realtime_data(payload)
    else:
        raise ValueError(f"Unsupported realtime host {api.host!r} for {api.dataset_name}")

    return _json(
        {
            "dataset_name": api.dataset_name,
            "title": api.title,
            "parameters": parameters or {},
            "data": data,
        }
    )
