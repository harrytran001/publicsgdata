# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.2](https://github.com/harrytran001/publicsgdata/compare/publicsgdata-v0.2.1...publicsgdata-v0.2.2) (2026-06-10)


### Bug Fixes

* point PyPI project URLs at the correct GitHub repository ([9b9ce67](https://github.com/harrytran001/publicsgdata/commit/9b9ce67e45dd6c729f3ec06fb35705143afe999c))
* point PyPI project URLs at the correct GitHub repository ([5571c54](https://github.com/harrytran001/publicsgdata/commit/5571c54eaf89b419c1fbb4ed8d02c6e2c04207b9))

## [0.2.1](https://github.com/harrytran001/publicsgdata/compare/publicsgdata-v0.2.0...publicsgdata-v0.2.1) (2026-06-09)


### Bug Fixes

* allow URL-only download poll responses ([c83a020](https://github.com/harrytran001/publicsgdata/commit/c83a0209a2ac7387942a76640361ba0844b3f694))
* allow URL-only download poll responses ([27c5d45](https://github.com/harrytran001/publicsgdata/commit/27c5d451dbd7c7676aadef0b724e72543457378f))

## [0.2.0](https://github.com/harrytran001/publicsgdata/compare/publicsgdata-v0.1.2...publicsgdata-v0.2.0) (2026-06-09)


### Features

* add dataset download API to publicsgdata SDK. ([0494d23](https://github.com/harrytran001/publicsgdata/commit/0494d23b53e7fa53002b608e9d45748a7c14903e))
* refactor packages + add mcp server ([272ad97](https://github.com/harrytran001/publicsgdata/commit/272ad97e809413fe07b9ac0a8c1d5ebcbbed8d56))

## [0.1.2](https://github.com/harrytran001/publicsgdata/compare/v0.1.1...v0.1.2) (2026-06-09)


### Documentation

* add unofficial project disclaimer to README ([08bbba7](https://github.com/harrytran001/publicsgdata/commit/08bbba72bff931942ce54ccbadce2d4ed868d9ae))
* add unofficial project disclaimer to README ([a24592e](https://github.com/harrytran001/publicsgdata/commit/a24592edd41749ee3efce41dd788506e2fb2ab91))

## [0.1.1](https://github.com/harrytran001/publicsgdata/compare/v0.1.0...v0.1.1) (2026-06-09)


### Documentation

* humanize copy and use uv for install ([05d227e](https://github.com/harrytran001/publicsgdata/commit/05d227e807bfa61e56a529f0c510e23503eed660))
* improve README quickstart examples ([dcda6f6](https://github.com/harrytran001/publicsgdata/commit/dcda6f667f53889d6b11089745c4f31c873aaa13))

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
