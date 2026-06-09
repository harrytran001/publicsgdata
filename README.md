# publicsgdata

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Python client for Singapore government open data: data.gov.sg today, LTA and OneMap later.

## Install

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
uv pip install publicsgdata
```

## Quickstart

```python
from publicsgdata import DataGovSGClient

with DataGovSGClient() as client:  # optional: api_key="..." or DATA_GOV_SG_API_KEY
    catalog = client.collections.list()
    print(f"{len(catalog.collections)} collections")
    print(catalog.collections[0].name)

    # HDB resale prices (swap in any dataset ID)
    rows = client.datasets.list_rows("d_8b84c4ee58e3cfc0ece0d773c8ca6abc", limit=10)
    for row in rows.rows:
        print(row.model_dump())

    pm25 = client.realtime.pm25.get()
    print(pm25.items[0].readings)
```

### Async

```python
from publicsgdata import AsyncDataGovSGClient

async with AsyncDataGovSGClient() as client:
    rows = await client.datasets.list_rows("d_8b84c4ee58e3cfc0ece0d773c8ca6abc", limit=5)
    print(len(rows.rows))
```

### Custom HTTP client

Pass your own `httpx` client if you need custom timeouts, proxies, etc.

```python
import httpx
from publicsgdata import DataGovSGClient

with httpx.Client(timeout=30.0) as http:
    client = DataGovSGClient(http_client=http)
    print(len(client.collections.list().collections))
```

## Authentication

You can call the API without a key while experimenting. For regular use, get a key from [data.gov.sg](https://data.gov.sg/) and set:

```bash
export DATA_GOV_SG_API_KEY="your-key"
```

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `DATA_GOV_SG_API_KEY` | No | data.gov.sg API key (`x-api-key` header) |

## Development

You'll need [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
./scripts/dev_setup.sh         # creates .venv from uv.lock
./scripts/format.sh
./scripts/validate.sh
./scripts/test.sh              # unit tests, runs in CI
./scripts/test_integration.sh  # hits the real API, local only
```

Or run things directly: `uv run pytest`, `uv run ruff check .`, etc.

See [CONTRIBUTING.md](CONTRIBUTING.md) if you're opening a PR.

## Roadmap

- **v0.1.0**: `DataGovSGClient`
- **v0.2.0**: `LTAClient` (LTA DataMall)
- **v0.3.0**: `OneMapClient`

## License

MIT. See [LICENSE](LICENSE).
