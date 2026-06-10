# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.2](https://github.com/harrytran001/publicsgdata/compare/publicsgdata-mcp-v0.2.1...publicsgdata-mcp-v0.2.2) (2026-06-10)


### Bug Fixes

* point PyPI project URLs at the correct GitHub repository ([9b9ce67](https://github.com/harrytran001/publicsgdata/commit/9b9ce67e45dd6c729f3ec06fb35705143afe999c))
* point PyPI project URLs at the correct GitHub repository ([5571c54](https://github.com/harrytran001/publicsgdata/commit/5571c54eaf89b419c1fbb4ed8d02c6e2c04207b9))

## [0.2.1](https://github.com/harrytran001/publicsgdata/compare/publicsgdata-mcp-v0.2.0...publicsgdata-mcp-v0.2.1) (2026-06-09)


### Bug Fixes

* allow URL-only download poll responses ([c83a020](https://github.com/harrytran001/publicsgdata/commit/c83a0209a2ac7387942a76640361ba0844b3f694))
* allow URL-only download poll responses ([27c5d45](https://github.com/harrytran001/publicsgdata/commit/27c5d451dbd7c7676aadef0b724e72543457378f))
* avoid Python 3.14 for MCP server ([44be9fa](https://github.com/harrytran001/publicsgdata/commit/44be9fae0f8fba4b5943297569983ff4e9141fae))
* mcp python 314 compat ([8614684](https://github.com/harrytran001/publicsgdata/commit/8614684a3ba399e886a82a786be9ee276978f5a4))


### Documentation

* keep MCP uvx config generic ([0c249ec](https://github.com/harrytran001/publicsgdata/commit/0c249ece2c22b9dc35ecf750a6f017e03ab952b5))

## [0.2.0](https://github.com/harrytran001/publicsgdata/compare/publicsgdata-mcp-v0.1.0...publicsgdata-mcp-v0.2.0) (2026-06-09)


### Features

* add publicsgdata-mcp local stdio server. ([d72a155](https://github.com/harrytran001/publicsgdata/commit/d72a155fde4d6634023065dc54025a396fbd9ffa))
* generalize realtime MCP tools ([c9d2d36](https://github.com/harrytran001/publicsgdata/commit/c9d2d36104e7d9518b81de2278d448ea18990b51))
* refactor packages + add mcp server ([272ad97](https://github.com/harrytran001/publicsgdata/commit/272ad97e809413fe07b9ac0a8c1d5ebcbbed8d56))

## [Unreleased]

## [0.1.0] - 2026-06-09

### Added

- Local stdio MCP server for data.gov.sg catalog preview, search, and full dataset download
- Tools: `list_datasets`, `get_dataset_metadata`, `preview_dataset_rows`, `search_dataset_rows`, `get_dataset_download_url`, `download_dataset_file`, `list_realtime_datasets`, `describe_realtime_dataset`, `fetch_realtime_data`
