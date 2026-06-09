from __future__ import annotations

import json
from collections.abc import Generator
from pathlib import Path
from unittest.mock import patch

import httpx
import pytest

from publicsgdata_mcp import tools


@pytest.fixture(autouse=True)
def reset_client() -> Generator[None, None, None]:
    tools.close_client()
    yield
    tools.close_client()


def test_list_datasets() -> None:
    fixture = {
        "code": 0,
        "data": {
            "datasets": [
                {
                    "datasetId": "d_test",
                    "name": "Test Dataset",
                }
            ]
        },
        "errorMsg": "",
    }

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/datasets"):
            return httpx.Response(200, json=fixture)
        return httpx.Response(404, json={"message": "not found"})

    transport = httpx.MockTransport(handler)
    with patch.object(tools, "get_client") as mock_get_client:
        from publicsgdata import DataGovSGClient

        client = DataGovSGClient(http_client=httpx.Client(transport=transport))
        mock_get_client.return_value = client
        payload = json.loads(tools.list_datasets())
        assert payload["datasets"][0]["dataset_id"] == "d_test"
        client.close()


def test_download_dataset_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PUBLICSGDATA_MCP_CACHE_DIR", str(tmp_path))

    initiate = {"code": 0, "data": {"message": "ok"}, "errorMsg": ""}
    poll = {
        "code": 0,
        "data": {"status": "READY", "url": "https://example.com/data.csv"},
        "errorMsg": "",
    }
    metadata = {
        "code": 0,
        "data": {
            "datasetId": "d_test",
            "name": "Test Dataset",
            "format": "CSV",
        },
        "errorMsg": "",
    }

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if path.endswith("/initiate-download"):
            return httpx.Response(200, json=initiate)
        if path.endswith("/poll-download"):
            return httpx.Response(200, json=poll)
        if path.endswith("/metadata"):
            return httpx.Response(200, json=metadata)
        if request.url.host == "example.com":
            return httpx.Response(200, content=b"col\n1\n")
        return httpx.Response(404, json={"message": "not found"})

    transport = httpx.MockTransport(handler)
    with patch.object(tools, "get_client") as mock_get_client:
        from publicsgdata import DataGovSGClient

        client = DataGovSGClient(http_client=httpx.Client(transport=transport))
        mock_get_client.return_value = client
        payload = json.loads(tools.download_dataset_file("d_test"))
        assert payload["dataset_id"] == "d_test"
        assert payload["local_path"].endswith("d_test.csv")
        assert (tmp_path / "datasets" / "d_test" / "d_test.csv").exists()
        client.close()
