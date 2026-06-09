#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [ ! -f uv.lock ]; then
  "$ROOT/scripts/dev_setup.sh"
fi

uv run pytest -m "not integration" --cov=publicsgdata --cov-report=term-missing packages/publicsgdata/tests packages/publicsgdata-mcp/tests "$@"
