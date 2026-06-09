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

## Releases (Release Please + PyPI)

1. Merge PRs with conventional titles (`feat:`, `fix:`, etc.).
2. Release Please opens a release PR updating `CHANGELOG.md` and `pyproject.toml`.
3. Merge the release PR → GitHub Release is created with notes.
4. `release.yml` publishes to TestPyPI then PyPI.

Configure secrets once: `PYPI_API_TOKEN`, `TEST_PYPI_API_TOKEN`.

Manual fallback:

```bash
gh release create v0.1.0 --title "v0.1.0" --notes-file CHANGELOG.md
```
