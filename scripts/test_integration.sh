#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [ ! -f uv.lock ]; then
  "$ROOT/scripts/dev_setup.sh"
fi

echo "Running live integration tests against data.gov.sg (network required)..."
uv run pytest -m integration -v "$@"
