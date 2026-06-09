> **Disclaimer:** This is not an official Singapore Government project. It is an independent open-source library and is not affiliated with, endorsed by, or operated by any government agency.

# publicsgdata

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Monorepo for Singapore government open data tools.

## Packages

| Package | Description |
|---------|-------------|
| [`publicsgdata`](packages/publicsgdata/) | Python SDK for data.gov.sg (and LTA / OneMap later) |

## Install

```bash
uv pip install publicsgdata
```

## Development

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
./scripts/dev_setup.sh         # creates .venv from uv.lock
./scripts/format.sh
./scripts/validate.sh
./scripts/test.sh              # unit tests, runs in CI
./scripts/test_integration.sh  # hits the real API, local only
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for PR guidelines.

## Repository layout

```text
packages/
  publicsgdata/        # Python SDK
scripts/               # repo-wide dev scripts
```

## License

MIT. See [LICENSE](LICENSE).
