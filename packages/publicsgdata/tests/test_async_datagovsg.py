import pytest

from publicsgdata.datagovsg.async_client import AsyncDataGovSGClient


@pytest.mark.asyncio
async def test_async_collections(async_client: AsyncDataGovSGClient) -> None:
    response = await async_client.collections.list()
    assert response.collections[0].collection_id == "471"


@pytest.mark.asyncio
async def test_async_pm25(async_client: AsyncDataGovSGClient) -> None:
    pm25 = await async_client.realtime.pm25.get()
    assert len(pm25.region_metadata) == 1


@pytest.mark.asyncio
async def test_async_dataset_poll_download_accepts_url_only_response(
    async_client: AsyncDataGovSGClient,
) -> None:
    result = await async_client.datasets.poll_download(
        "d_8b84c4ee58e3cfc0ece0d773c8ca6abc"
    )
    assert result.status is None
    assert result.url == "https://example.com/datasets/hdb-resale.csv"
