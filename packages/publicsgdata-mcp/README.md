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
| `get_pm25` | Realtime PM2.5 readings |

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
