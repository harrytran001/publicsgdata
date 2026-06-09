# publicsgdata

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Python SDK for Singapore government public data

## Install

```bash
pip install publicsgdata
```

## Quickstart

```python
from publicsgdata import DataGovSGClient

with DataGovSGClient() as client:  # optional: api_key="..." or DATA_GOV_SG_API_KEY env
    # Browse catalog collections
    catalog = client.collections.list()
    print(f"{len(catalog.collections)} collections")
    print(catalog.collections[0].name)

    # Fetch dataset rows (HDB resale prices example dataset)
    rows = client.datasets.list_rows("d_8b84c4ee58e3cfc0ece0d773c8ca6abc", limit=10)
    for row in rows.rows:
        print(row.model_dump())

    # PM2.5 real-time readings
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

### Bring your own HTTP client

```python
import httpx
from publicsgdata import DataGovSGClient

with httpx.Client(timeout=30.0) as http:
    client = DataGovSGClient(http_client=http)
    print(client.collections.list())
```

## Authentication

data.gov.sg APIs work without a key for testing. For production, register an API key at [data.gov.sg](https://data.gov.sg/) and set:

```bash
export DATA_GOV_SG_API_KEY="your-key"
```

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `DATA_GOV_SG_API_KEY` | No | data.gov.sg API key (`x-api-key` header) |

## Development

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
./scripts/dev_setup.sh         # uv sync — creates .venv from uv.lock
./scripts/format.sh
./scripts/validate.sh
./scripts/test.sh              # unit tests (CI)
./scripts/test_integration.sh  # live API smoke tests (local only)
```

Or run tools directly: `uv run pytest`, `uv run ruff check .`, etc.

See [CONTRIBUTING.md](CONTRIBUTING.md) for PR guidelines and release process.

## Roadmap

- **v0.1.0** — `DataGovSGClient` (this release)
- **v0.2.0** — `LTAClient` (LTA DataMall)
- **v0.3.0** — `OneMapClient`

## License

MIT — see [LICENSE](LICENSE).
