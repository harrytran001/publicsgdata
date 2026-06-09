# publicsgdata-mcp

Local [Model Context Protocol](https://modelcontextprotocol.io/) server for exploring and downloading Singapore government open data through the `publicsgdata` SDK.

## Cursor config

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "publicsgdata": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--python", "3.12", "publicsgdata-mcp"],
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

Downloads are cached under `~/.cache/publicsgdata-mcp` by default. Override with `PUBLICSGDATA_MCP_CACHE_DIR`.

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATA_GOV_SG_API_KEY` | No | Higher rate limits for data.gov.sg |
| `PUBLICSGDATA_MCP_CACHE_DIR` | No | Override download cache directory |
