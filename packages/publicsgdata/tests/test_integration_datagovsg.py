"""Live API tests. Run locally, not in CI. Needs network.

Set DATA_GOV_SG_API_KEY if you hit rate limits.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator, Generator

import pytest

from publicsgdata import DataGovSGClient
from publicsgdata.datagovsg.async_client import AsyncDataGovSGClient

# Stable public datasets used as smoke-test fixtures
HDB_RESALE_DATASET_ID = "d_8b84c4ee58e3cfc0ece0d773c8ca6abc"
COLLECTION_ID = "471"

pytestmark = pytest.mark.integration


@pytest.fixture
def live_client() -> Generator[DataGovSGClient, None, None]:
    client = DataGovSGClient()
    yield client
    client.close()


@pytest.fixture
async def live_async_client() -> AsyncGenerator[AsyncDataGovSGClient, None]:
    client = AsyncDataGovSGClient()
    yield client
    await client.close()


def test_live_collections_list(live_client: DataGovSGClient) -> None:
    response = live_client.collections.list()
    assert len(response.collections) >= 1


def test_live_collection_metadata(live_client: DataGovSGClient) -> None:
    metadata = live_client.collections.get_metadata(COLLECTION_ID)
    assert metadata.collection_id == COLLECTION_ID
    assert metadata.name


def test_live_dataset_metadata(live_client: DataGovSGClient) -> None:
    metadata = live_client.datasets.get_metadata(HDB_RESALE_DATASET_ID)
    assert metadata.dataset_id == HDB_RESALE_DATASET_ID
    assert "resale" in metadata.name.lower()


def test_live_dataset_list_rows(live_client: DataGovSGClient) -> None:
    rows = live_client.datasets.list_rows(HDB_RESALE_DATASET_ID, limit=3)
    assert len(rows.rows) >= 1
    assert rows.rows[0].model_dump().get("town")


def test_live_dataset_search(live_client: DataGovSGClient) -> None:
    result = live_client.datasets.search(HDB_RESALE_DATASET_ID, limit=2, q="ANG MO KIO")
    assert result.total >= 1
    assert len(result.records) >= 1


def test_live_pm25(live_client: DataGovSGClient) -> None:
    pm25 = live_client.realtime.pm25.get()
    assert len(pm25.items) >= 1
    assert pm25.items[0].readings is not None


@pytest.mark.asyncio
async def test_live_async_collections(live_async_client: AsyncDataGovSGClient) -> None:
    response = await live_async_client.collections.list()
    assert len(response.collections) >= 1
