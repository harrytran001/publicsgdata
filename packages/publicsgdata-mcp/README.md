# publicsgdata-mcp

Local [Model Context Protocol](https://modelcontextprotocol.io/) server for exploring and downloading Singapore government open data through the `publicsgdata` SDK.

## Install

```bash
uv pip install publicsgdata-mcp
```

From the monorepo root:

```bash
uv sync
uv run publicsgdata-mcp
```

## Cursor config

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "publicsgdata": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/publicsgdata",
        "publicsgdata-mcp"
      ],
      "env": {
        "DATA_GOV_SG_API_KEY": "${env:DATA_GOV_SG_API_KEY}"
      }
    }
  }
}
```

After publishing:

```json
{
  "mcpServers": {
    "publicsgdata": {
      "type": "stdio",
      "command": "uvx",
      "args": ["publicsgdata-mcp"],
      "env": {
        "DATA_GOV_SG_API_KEY": "${env:DATA_GOV_SG_API_KEY}"
      }
    }
  }
}
```

## Tools

| Tool | Purpose |
|------|---------|
| `list_datasets` | Browse the catalog |
| `get_dataset_metadata` | Schema, size, coverage |
| `preview_dataset_rows` | Small sample for inspection |
| `search_dataset_rows` | Filter/search within a dataset |
| `get_dataset_download_url` | Temporary URL for full export |
| `download_dataset_file` | Save full dataset locally |
| `list_realtime_datasets` | List supported realtime dataset names |
| `describe_realtime_dataset` | Full parameter and response docs for one realtime dataset |
| `fetch_realtime_data` | Fetch data from a realtime API by `dataset_name` |

## Realtime APIs

Instead of one MCP tool per realtime endpoint, use a three-step flow:

1. **`list_realtime_datasets`** — returns descriptive `dataset_name` strings.
2. **`describe_realtime_dataset`** — pass a `dataset_name` (e.g. `air_quality_pm25_hourly_by_region`) for full parameter and response documentation.
3. **`fetch_realtime_data`** — pass the same `dataset_name` and optional `parameters` dict (e.g. `{"date": "2024-07-16"}`).

New realtime endpoints are added to the catalog in code; agents do not need new tools when more APIs are supported.

## Agent workflow

1. Call `get_dataset_metadata` and `preview_dataset_rows` to understand the dataset.
2. Call `download_dataset_file` when full analysis is needed.
3. Use the returned `local_path` with local Python, DuckDB, pandas, or other agent tools.

Downloads are cached under `~/.cache/publicsgdata-mcp` by default. Override with `PUBLICSGDATA_MCP_CACHE_DIR`.

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATA_GOV_SG_API_KEY` | No | Higher rate limits for data.gov.sg |
| `PUBLICSGDATA_MCP_CACHE_DIR` | No | Override download cache directory |
