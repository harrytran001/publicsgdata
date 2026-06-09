# Contributing to publicsgdata

Contributions are welcome. Please follow the fork and pull request workflow.

## Pull request guidelines

1. **Title format** — must match one of:
   - `[feat] Add dataset download helper`
   - `feat: Add dataset download helper`
   - `feat-dataset-download`
2. **Link issues** — use `fixes #123` in the description when applicable.
3. **No duplicate PRs** — search [open pull requests](https://github.com/publicsgdata/publicsgdata/pulls) first.
4. **AI-generated PRs** — disclose in the PR template if entirely AI-generated.

PR titles are enforced by `.github/workflows/pr-lint.yml`.

## Development setup

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
./scripts/dev_setup.sh   # uv sync
```

Run tools via `uv run` (e.g. `uv run pytest`) or use the `./scripts/*.sh` helpers.

## Formatting and validation

```bash
./scripts/format.sh
./scripts/validate.sh
```

## Tests

**Unit tests (mocked, runs in CI):**

```bash
./scripts/test.sh
```

**Integration tests (live data.gov.sg API, local only — not in CI):**

```bash
./scripts/test_integration.sh
```

Requires network. Optional: `export DATA_GOV_SG_API_KEY=...` for higher rate limits.
