from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from publicsgdata_mcp import tools

mcp = FastMCP("publicsgdata")


@mcp.tool()
def list_datasets(page: int | None = None) -> str:
    """List datasets available on data.gov.sg."""
    return tools.list_datasets(page=page)


@mcp.tool()
def get_dataset_metadata(dataset_id: str) -> str:
    """Get metadata for a dataset by its dataset ID."""
    return tools.get_dataset_metadata(dataset_id)


@mcp.tool()
def preview_dataset_rows(
    dataset_id: str,
    limit: int = 10,
    cursor: str | None = None,
) -> str:
    """Preview a bounded number of rows from a dataset."""
    return tools.preview_dataset_rows(dataset_id, limit=limit, cursor=cursor)


@mcp.tool()
def search_dataset_rows(
    dataset_id: str,
    q: str | None = None,
    sort: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> str:
    """Search rows within a dataset using CKAN datastore search."""
    return tools.search_dataset_rows(dataset_id, q=q, sort=sort, limit=limit, offset=offset)


@mcp.tool()
def get_dataset_download_url(dataset_id: str, skip_initiate: bool = False) -> str:
    """Get a temporary download URL for the full dataset."""
    return tools.get_dataset_download_url(dataset_id, skip_initiate=skip_initiate)


@mcp.tool()
def download_dataset_file(dataset_id: str, filename: str | None = None) -> str:
    """Download the full dataset to a local cache file and return the local path."""
    return tools.download_dataset_file(dataset_id, filename=filename)


@mcp.tool()
def get_pm25(date: str | None = None) -> str:
    """Get PM2.5 readings. Optionally pass a date like 2024-07-16."""
    return tools.get_pm25(date=date)


def main() -> None:
    try:
        mcp.run(transport="stdio")
    finally:
        tools.close_client()


if __name__ == "__main__":
    main()
