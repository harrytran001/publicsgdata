# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-06-09

### Added

- `DataGovSGClient` and `AsyncDataGovSGClient`: sync and async, with optional custom `httpx` clients
- `collections.list()` and `collections.get_metadata()`
- `datasets.list()`, `get_metadata()`, `list_rows()`, `iter_rows()`, and CKAN `search()`
- `realtime.pm25.get()` for PM2.5 readings
- Pydantic v2 response models
- Optional `DATA_GOV_SG_API_KEY` auth via `x-api-key` header
- CI, release-please, and PyPI publish workflows

[0.1.0]: https://github.com/publicsgdata/publicsgdata/releases/tag/v0.1.0
