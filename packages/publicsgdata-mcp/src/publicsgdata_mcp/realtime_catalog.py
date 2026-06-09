from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RealtimeParameter:
    name: str
    type: str
    required: bool
    description: str
    example: str | None = None


@dataclass(frozen=True)
class RealtimeResponseField:
    name: str
    type: str
    description: str


@dataclass(frozen=True)
class RealtimeApiDefinition:
    dataset_name: str
    title: str
    summary: str
    description: str
    path: str
    host: str
    update_frequency: str | None
    parameters: tuple[RealtimeParameter, ...]
    response_fields: tuple[RealtimeResponseField, ...]
    response_notes: str
    dataset_url: str | None = None
    aliases: tuple[str, ...] = ()


REALTIME_APIS: tuple[RealtimeApiDefinition, ...] = (
    RealtimeApiDefinition(
        dataset_name="air_quality_pm25_hourly_by_region",
        title="PM2.5 hourly readings by region",
        summary="Hourly PM2.5 air quality readings for Singapore regions from NEA.",
        description=(
            "Returns the latest or historical PM2.5 readings from the data.gov.sg v2 "
            "real-time API. Readings are grouped by major regions such as north, south, "
            "east, west, and central, with map label coordinates in region_metadata."
        ),
        path="/pm25",
        host="v2_realtime",
        update_frequency="Hourly",
        parameters=(
            RealtimeParameter(
                name="date",
                type="string",
                required=False,
                description=(
                    "SGT date or datetime filter. Use YYYY-MM-DD for all readings on a day, "
                    "or YYYY-MM-DDTHH:MM:SS for readings at a specific moment. "
                    "Omit to fetch the latest reading."
                ),
                example="2024-07-16",
            ),
            RealtimeParameter(
                name="paginationToken",
                type="string",
                required=False,
                description=(
                    "Pagination token from a previous response when requesting a full day "
                    "or large historical range."
                ),
            ),
        ),
        response_fields=(
            RealtimeResponseField(
                name="region_metadata",
                type="array",
                description="Regions with name and labelLocation latitude/longitude for mapping.",
            ),
            RealtimeResponseField(
                name="items",
                type="array",
                description=(
                    "Reading snapshots. Each item includes date, timestamp, "
                    "updatedTimestamp, and readings.pm25_one_hourly by region."
                ),
            ),
            RealtimeResponseField(
                name="pagination_token",
                type="string|null",
                description="Token for the next page when more historical readings exist.",
            ),
        ),
        response_notes="Units are µg/m3. Latest reading is returned when date is omitted.",
        dataset_url="https://data.gov.sg/datasets?formats=API",
        aliases=("pm25", "pm2_5", "air_quality"),
    ),
)


def _index_apis() -> dict[str, RealtimeApiDefinition]:
    indexed: dict[str, RealtimeApiDefinition] = {}
    for api in REALTIME_APIS:
        indexed[api.dataset_name.lower()] = api
        for alias in api.aliases:
            indexed[alias.lower()] = api
    return indexed


_API_INDEX = _index_apis()


def list_realtime_dataset_names() -> list[str]:
    return [api.dataset_name for api in REALTIME_APIS]


def resolve_realtime_api(dataset_name: str) -> RealtimeApiDefinition:
    key = dataset_name.strip().lower()
    api = _API_INDEX.get(key)
    if api is None:
        known = ", ".join(list_realtime_dataset_names())
        raise ValueError(
            f"Unknown realtime dataset_name {dataset_name!r}. Known datasets: {known}"
        )
    return api


def describe_realtime_api(dataset_name: str) -> dict[str, Any]:
    api = resolve_realtime_api(dataset_name)
    return {
        "dataset_name": api.dataset_name,
        "title": api.title,
        "summary": api.summary,
        "description": api.description,
        "host": api.host,
        "path": api.path,
        "update_frequency": api.update_frequency,
        "dataset_url": api.dataset_url,
        "aliases": list(api.aliases),
        "parameters": [
            {
                "name": param.name,
                "type": param.type,
                "required": param.required,
                "description": param.description,
                "example": param.example,
            }
            for param in api.parameters
        ],
        "response_fields": [
            {
                "name": field.name,
                "type": field.type,
                "description": field.description,
            }
            for field in api.response_fields
        ],
        "response_notes": api.response_notes,
        "example_request": {
            "dataset_name": api.dataset_name,
            "parameters": {
                param.name: param.example
                for param in api.parameters
                if param.example is not None
            },
        },
    }


def normalize_realtime_parameters(
    api: RealtimeApiDefinition,
    parameters: dict[str, Any] | None,
) -> dict[str, str]:
    incoming = parameters or {}
    allowed = {param.name for param in api.parameters}
    unknown = sorted(set(incoming) - allowed)
    if unknown:
        raise ValueError(
            f"Unknown parameters for {api.dataset_name}: {unknown}. "
            f"Allowed: {sorted(allowed)}"
        )

    missing = [
        param.name
        for param in api.parameters
        if param.required and param.name not in incoming
    ]
    if missing:
        raise ValueError(f"Missing required parameters for {api.dataset_name}: {missing}")

    encoded: dict[str, str] = {}
    for key, value in incoming.items():
        if value is not None:
            encoded[key] = str(value)
    return encoded
