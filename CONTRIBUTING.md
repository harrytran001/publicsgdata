# Contributing

Fork the repo, make your changes, open a pull request.

## Pull requests

1. **Title**: pick one of these formats:
   - `[feat] Add dataset download helper`
   - `feat: Add dataset download helper`
   - `feat-dataset-download`
2. **Issues**: add `fixes #123` in the description when it applies.
3. **Duplicates**: check [open PRs](https://github.com/publicsgdata/publicsgdata/pulls) first.
4. **AI-assisted work**: mention it in the PR template if the whole PR was generated.

Titles are checked by `.github/workflows/pr-lint.yml`.

## Setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```bash
./scripts/dev_setup.sh
```

Use `uv run pytest` (and friends) or the `./scripts/*.sh` scripts from the repo root.

## Repository layout

```text
packages/
  publicsgdata/        # Python SDK
```

## Formatting

```bash
./scripts/format.sh
./scripts/validate.sh
```

## Tests

Unit tests (mocked, runs in CI):

```bash
./scripts/test.sh
```

Integration tests (real API, not in CI):

```bash
./scripts/test_integration.sh
```

Needs network. Set `DATA_GOV_SG_API_KEY` if you hit rate limits.
