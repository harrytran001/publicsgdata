from __future__ import annotations

from typing import Annotated, Any

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from publicsgdata_mcp import tools

mcp = FastMCP("publicsgdata")

DatasetId = Annotated[
    str,
    Field(
        description=(
            "data.gov.sg dataset ID (starts with d_). "
            "Example: d_8b84c4ee58e3cfc0ece0d773c8ca6abc for HDB resale prices."
        ),
    ),
]


@mcp.tool()
def list_datasets(
    page: Annotated[
        int | None,
        Field(
            description="Optional 1-based catalog page number. Omit to fetch the first page.",
        ),
    ] = None,
) -> str:
    """List datasets available on data.gov.sg.

    Returns JSON:
    - datasets (list): Catalog entries with dataset_id, name, format, status, coverage dates
    - pages (int | null): Total catalog pages when paginated
    """
    return tools.list_datasets(page=page)


@mcp.tool()
def get_dataset_metadata(dataset_id: DatasetId) -> str:
    """Get metadata for a dataset, including column definitions when available.

    Returns JSON:
    - dataset_id (str): Dataset identifier
    - name (str): Dataset title
    - description (str | null): Dataset summary
    - format (str | null): File/API format, e.g. CSV
    - dataset_size (int | null): Approximate row count
    - coverage_start / coverage_end (str | null): Data time range
    - column_metadata (object | null): Column names and types for interpreting rows
    """
    return tools.get_dataset_metadata(dataset_id)


@mcp.tool()
def preview_dataset_rows(
    dataset_id: DatasetId,
    limit: Annotated[
        int,
        Field(
            description="Number of rows to preview. Capped at 50. Default 10.",
            ge=1,
            le=50,
        ),
    ] = 10,
    cursor: Annotated[
        str | None,
        Field(
            description=(
                "Pagination cursor from a previous response links.next value. "
                "Omit on the first request."
            ),
        ),
    ] = None,
) -> str:
    """Preview a bounded sample of rows from a dataset.

    Use this before downloading the full file. Row keys match the dataset columns.

    Returns JSON:
    - dataset_id (str): Requested dataset ID
    - dataset_name (str | null): Dataset title
    - rows (list[object]): Sample records; each object is one row keyed by column name
    - limit (int): Applied row limit
    - links.next (str | null): Cursor for the next page, if more rows exist
    """
    return tools.preview_dataset_rows(dataset_id, limit=limit, cursor=cursor)


@mcp.tool()
def search_dataset_rows(
    dataset_id: DatasetId,
    q: Annotated[
        str | None,
        Field(
            description=(
                "Full-text search query for CKAN datastore_search. "
                "Use column values that make sense for the dataset."
            ),
        ),
    ] = None,
    filters: Annotated[
        dict[str, Any] | None,
        Field(
            description=(
                "Exact-match filters keyed by column name, e.g. {'town': 'ANG MO KIO'}. "
                "Use column names from get_dataset_metadata."
            ),
        ),
    ] = None,
    sort: Annotated[
        str | None,
        Field(
            description=(
                "Sort order for results, e.g. 'month desc'. "
                "Use column names from get_dataset_metadata."
            ),
        ),
    ] = None,
    limit: Annotated[
        int,
        Field(
            description="Maximum matching rows to return. Capped at 50. Default 20.",
            ge=1,
            le=50,
        ),
    ] = 20,
    offset: Annotated[
        int,
        Field(
            description="Number of matching rows to skip for pagination. Default 0.",
            ge=0,
        ),
    ] = 0,
) -> str:
    """Search rows within a dataset using CKAN datastore search.

    Returns JSON:
    - resource_id (str): Dataset resource ID searched
    - fields (list): Column id/type definitions for the records
    - records (list[object]): Matching rows keyed by column name
    - total (int): Total matches for the query
    - limit (int): Applied page size
    - offset (int): Applied offset
    - links.next (str | null): Relative URL for the next page, if any
    """
    return tools.search_dataset_rows(
        dataset_id,
        q=q,
        filters=filters,
        sort=sort,
        limit=limit,
        offset=offset,
    )


@mcp.tool()
def get_dataset_download_url(
    dataset_id: DatasetId,
    skip_initiate: Annotated[
        bool,
        Field(
            description=(
                "Poll for an existing export without first requesting a CSV export. "
                "Useful for non-CSV datasets such as GeoJSON or KML."
            ),
        ),
    ] = False,
) -> str:
    """Get a temporary URL for the full dataset export.

    Returns JSON:
    - dataset_id (str): Requested dataset ID
    - url (str): Temporary download URL valid for a short period
    """
    return tools.get_dataset_download_url(dataset_id, skip_initiate=skip_initiate)


@mcp.tool()
def download_dataset_file(
    dataset_id: DatasetId,
    filename: Annotated[
        str | None,
        Field(
            description=(
                "Optional local filename under the MCP cache directory. "
                "Defaults to {dataset_id}.csv."
            ),
        ),
    ] = None,
    skip_initiate: Annotated[
        bool,
        Field(
            description=(
                "Poll for an existing export without first requesting a CSV export. "
                "Useful for non-CSV datasets such as GeoJSON or KML."
            ),
        ),
    ] = False,
) -> str:
    """Download the full dataset to a local cache file for offline analysis.

    Returns JSON:
    - dataset_id (str): Requested dataset ID
    - local_path (str): Absolute path to the downloaded file on this machine
    - name (str): Dataset title
    - format (str | null): Dataset format, e.g. CSV
    """
    return tools.download_dataset_file(
        dataset_id,
        filename=filename,
        skip_initiate=skip_initiate,
    )


@mcp.tool()
def list_realtime_datasets() -> str:
    """List supported realtime dataset names.

    Returns JSON: array of descriptive dataset_name strings.
    """
    return tools.list_realtime_datasets()


@mcp.tool()
def describe_realtime_dataset(
    dataset_name: Annotated[
        str,
        Field(
            description=(
                "Descriptive realtime dataset name, "
                "e.g. air_quality_pm25_hourly_by_region."
            ),
        ),
    ],
) -> str:
    """Describe a realtime dataset's parameters and response fields.

    Returns JSON:
    - dataset_name (str): Canonical dataset identifier
    - title, summary, description (str): Human-readable dataset documentation
    - parameters (list): Allowed query parameters with types and descriptions
    - response_fields (list): Top-level response fields and their meanings
    - example_request (object): Example dataset_name and parameters
    """
    return tools.describe_realtime_dataset(dataset_name=dataset_name)


@mcp.tool()
def fetch_realtime_data(
    dataset_name: Annotated[
        str,
        Field(
            description=(
                "Descriptive realtime dataset name, "
                "e.g. air_quality_pm25_hourly_by_region."
            ),
        ),
    ],
    parameters: Annotated[
        dict[str, Any] | None,
        Field(
            description=(
                "Query parameters for the chosen realtime dataset. Keys must match "
                "the parameter names returned by describe_realtime_dataset, such as date "
                "or paginationToken."
            ),
        ),
    ] = None,
) -> str:
    """Fetch data from a data.gov.sg realtime API.

    Returns JSON:
    - dataset_name (str): Resolved dataset identifier
    - title (str): Human-readable dataset title
    - parameters (object): Parameters sent to the API
    - data (object): Raw realtime payload from data.gov.sg
    """
    return tools.fetch_realtime_data(dataset_name=dataset_name, parameters=parameters)


def main() -> None:
    try:
        mcp.run(transport="stdio")
    finally:
        tools.close_client()


if __name__ == "__main__":
    main()
