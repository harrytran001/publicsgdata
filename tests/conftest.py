from __future__ import annotations

import json
from collections.abc import AsyncGenerator, Generator
from pathlib import Path
from typing import Any, cast

import httpx
import pytest

from publicsgdata import DataGovSGClient
from publicsgdata.datagovsg.async_client import AsyncDataGovSGClient

FIXTURES = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((FIXTURES / name).read_text()))


def mock_handler(request: httpx.Request) -> httpx.Response:
    path = request.url.path
    if path.endswith("/collections") and "/metadata" not in path:
        return httpx.Response(200, json=load_fixture("collections_list.json"))
    if "/collections/" in path and path.endswith("/metadata"):
        return httpx.Response(200, json=load_fixture("collection_metadata.json"))
    if path.endswith("/list-rows"):
        return httpx.Response(200, json=load_fixture("dataset_rows.json"))
    if path.endswith("/datastore_search"):
        return httpx.Response(200, json=load_fixture("datastore_search.json"))
    if path.endswith("/pm25"):
        return httpx.Response(200, json=load_fixture("pm25.json"))
    return httpx.Response(404, json={"message": "not found"})


@pytest.fixture
def sync_client() -> Generator[DataGovSGClient, None, None]:
    transport = httpx.MockTransport(mock_handler)
    http_client = httpx.Client(transport=transport)
    client = DataGovSGClient(http_client=http_client, api_key="test-key")
    yield client
    client.close()


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncDataGovSGClient, None]:
    transport = httpx.MockTransport(mock_handler)
    http_client = httpx.AsyncClient(transport=transport)
    client = AsyncDataGovSGClient(http_client=http_client, api_key="test-key")
    yield client
    await client.close()
