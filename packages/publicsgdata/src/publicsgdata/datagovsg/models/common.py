from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ApiModel(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class PaginationLinks(ApiModel):
    next: str | None = None
    start: str | None = None


class DatasetRow(ApiModel):
    model_config = ConfigDict(extra="allow")


class CollectionSummary(ApiModel):
    collection_id: str = Field(alias="collectionId")
    name: str
    description: str | None = None
    created_at: str | None = Field(default=None, alias="createdAt")
    last_updated_at: str | None = Field(default=None, alias="lastUpdatedAt")
    frequency: str | None = None
    sources: list[str] | None = None
    managed_by_agency_name: str | None = Field(default=None, alias="managedByAgencyName")
    child_datasets: list[str] | None = Field(default=None, alias="childDatasets")


class CollectionMetadata(ApiModel):
    collection_id: str = Field(alias="collectionId")
    name: str
    description: str | None = None
    created_at: str | None = Field(default=None, alias="createdAt")
    last_updated_at: str | None = Field(default=None, alias="lastUpdatedAt")
    frequency: str | None = None
    sources: list[str] | None = None
    managed_by: str | None = Field(default=None, alias="managedBy")
    child_datasets: list[str] | None = Field(default=None, alias="childDatasets")


class CollectionListResponse(ApiModel):
    collections: list[CollectionSummary]


class CollectionMetadataResponse(ApiModel):
    collection_metadata: CollectionMetadata = Field(alias="collectionMetadata")


class DatasetSummary(ApiModel):
    dataset_id: str = Field(alias="datasetId")
    name: str
    status: str | None = None
    description: str | None = None
    format: str | None = None
    created_at: str | None = Field(default=None, alias="createdAt")
    last_updated_at: str | None = Field(default=None, alias="lastUpdatedAt")
    managed_by_agency_name: str | None = Field(default=None, alias="managedByAgencyName")
    coverage_start: str | None = Field(default=None, alias="coverageStart")
    coverage_end: str | None = Field(default=None, alias="coverageEnd")


class DatasetListResponse(ApiModel):
    datasets: list[DatasetSummary]
    pages: int | None = None


class DatasetMetadata(ApiModel):
    dataset_id: str = Field(alias="datasetId")
    name: str
    description: str | None = None
    format: str | None = None
    status: str | None = None
    created_at: str | None = Field(default=None, alias="createdAt")
    last_updated_at: str | None = Field(default=None, alias="lastUpdatedAt")
    managed_by: str | None = Field(default=None, alias="managedBy")
    collection_ids: list[str] | None = Field(default=None, alias="collectionIds")
    coverage_start: str | None = Field(default=None, alias="coverageStart")
    coverage_end: str | None = Field(default=None, alias="coverageEnd")
    contact_emails: list[str] | None = Field(default=None, alias="contactEmails")
    dataset_size: int | None = Field(default=None, alias="datasetSize")
    column_metadata: dict[str, Any] | None = Field(default=None, alias="columnMetadata")


class DatasetMetadataResponse(ApiModel):
    dataset_metadata: DatasetMetadata | None = Field(default=None, alias="datasetMetadata")

    @property
    def metadata(self) -> DatasetMetadata:
        if self.dataset_metadata is not None:
            return self.dataset_metadata
        raise ValueError("dataset metadata missing from response")


class DatasetRowsResponse(ApiModel):
    dataset_id: str = Field(alias="datasetId")
    dataset_name: str | None = Field(default=None, alias="datasetName")
    rows: list[DatasetRow]
    limit: int
    links: PaginationLinks | None = None


class DatastoreField(ApiModel):
    id: str
    type: str | None = None


class DatastoreSearchLinks(ApiModel):
    start: str | None = None
    next: str | None = None


class DatastoreSearchResult(ApiModel):
    resource_id: str
    fields: list[DatastoreField]
    records: list[DatasetRow]
    total: int
    limit: int
    offset: int = 0
    links: DatastoreSearchLinks = Field(default_factory=DatastoreSearchLinks)


class PM25Reading(ApiModel):
    date: str | None = None
    updated_timestamp: str | None = Field(default=None, alias="updatedTimestamp")
    timestamp: str | None = None
    readings: dict[str, Any] | None = None


class PM25RegionMetadata(ApiModel):
    name: str
    label_location: dict[str, float] | None = Field(default=None, alias="labelLocation")


class PM25Response(ApiModel):
    region_metadata: list[PM25RegionMetadata] = Field(default_factory=list, alias="regionMetadata")
    items: list[PM25Reading] = Field(default_factory=list)
    pagination_token: str | None = Field(default=None, alias="paginationToken")


class DownloadFilter(ApiModel):
    column_name: str = Field(alias="columnName")
    type: str
    value: str


class DownloadInitiateResponse(ApiModel):
    message: str | None = None


class DownloadPollResponse(ApiModel):
    status: str | None = None
    url: str | None = None
