# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.1.0 (2026-06-09)


### Features

* add DataGovSGClient SDK with uv-based dev workflow ([45d8b90](https://github.com/harrytran001/publicsgdata/commit/45d8b9040d503eb2440fdb995099d111afaf4c98))

## [Unreleased]

## [0.1.0] - 2026-06-09

### Added

- `DataGovSGClient` and `AsyncDataGovSGClient` with injectable `httpx` clients
- `collections.list()` and `collections.get_metadata()`
- `datasets.list()`, `get_metadata()`, `list_rows()`, `iter_rows()`, and CKAN `search()`
- `realtime.pm25.get()` for PM2.5 readings from data.gov.sg
- Pydantic v2 typed response models
- Optional `DATA_GOV_SG_API_KEY` authentication via `x-api-key` header
- Agno-style CI, release-please, and PyPI publish workflows

[0.1.0]: https://github.com/publicsgdata/publicsgdata/releases/tag/v0.1.0
