from __future__ import annotations

import os
from pathlib import Path

ENV_CACHE_DIR = "PUBLICSGDATA_MCP_CACHE_DIR"


def default_cache_dir() -> Path:
    override = os.environ.get(ENV_CACHE_DIR)
    if override:
        return Path(override).expanduser()
    return Path.home() / ".cache" / "publicsgdata-mcp"


def dataset_cache_path(dataset_id: str, *, filename: str | None = None) -> Path:
    cache_dir = default_cache_dir() / "datasets" / dataset_id
    cache_dir.mkdir(parents=True, exist_ok=True)
    if filename:
        return cache_dir / filename
    return cache_dir / f"{dataset_id}.csv"
