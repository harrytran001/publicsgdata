from pathlib import Path

from publicsgdata.datagovsg.client import DataGovSGClient


def test_collections_list(sync_client: DataGovSGClient) -> None:
    response = sync_client.collections.list()
    assert len(response.collections) == 1
    assert response.collections[0].collection_id == "471"


def test_collection_metadata(sync_client: DataGovSGClient) -> None:
    metadata = sync_client.collections.get_metadata("471")
    assert metadata.name == "TradeNet Service Centres"


def test_dataset_list_rows(sync_client: DataGovSGClient) -> None:
    rows = sync_client.datasets.list_rows("d_8b84c4ee58e3cfc0ece0d773c8ca6abc", limit=2)
    assert rows.limit == 2
    assert len(rows.rows) == 2
    assert rows.rows[0].model_dump()["town"] == "ANG MO KIO"


def test_dataset_iter_rows(sync_client: DataGovSGClient) -> None:
    iterator = sync_client.datasets.iter_rows("d_8b84c4ee58e3cfc0ece0d773c8ca6abc", limit=2)
    first = next(iterator)
    assert first.model_dump()["month"] == "2017-01"


def test_dataset_search(sync_client: DataGovSGClient) -> None:
    result = sync_client.datasets.search("d_8b84c4ee58e3cfc0ece0d773c8ca6abc", limit=1)
    assert result.total == 2
    assert len(result.records) == 1


def test_pm25(sync_client: DataGovSGClient) -> None:
    pm25 = sync_client.realtime.pm25.get()
    assert len(pm25.items) == 1
    assert pm25.items[0].readings is not None


def test_dataset_initiate_download(sync_client: DataGovSGClient) -> None:
    result = sync_client.datasets.initiate_download("d_8b84c4ee58e3cfc0ece0d773c8ca6abc")
    assert result.message == "Download initiated"


def test_dataset_poll_download_accepts_url_only_response(sync_client: DataGovSGClient) -> None:
    result = sync_client.datasets.poll_download("d_8b84c4ee58e3cfc0ece0d773c8ca6abc")
    assert result.status is None
    assert result.url == "https://example.com/datasets/hdb-resale.csv"


def test_dataset_get_download_url(sync_client: DataGovSGClient) -> None:
    url = sync_client.datasets.get_download_url(
        "d_8b84c4ee58e3cfc0ece0d773c8ca6abc",
        poll_interval=0.01,
    )
    assert url == "https://example.com/datasets/hdb-resale.csv"


def test_dataset_download_file(sync_client: DataGovSGClient, tmp_path: Path) -> None:
    path = sync_client.datasets.download_file(
        "d_8b84c4ee58e3cfc0ece0d773c8ca6abc",
        tmp_path / "hdb.csv",
        poll_interval=0.01,
    )
    assert path.exists()
    assert b"ANG MO KIO" in path.read_bytes()
