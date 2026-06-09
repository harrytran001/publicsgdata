from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from publicsgdata.datagovsg.models import DownloadFilter


def build_download_body(
    *,
    column_names: Sequence[str] | None = None,
    filters: Sequence[DownloadFilter | Mapping[str, Any]] | None = None,
) -> dict[str, Any] | None:
    body: dict[str, Any] = {}
    if column_names:
        body["columnNames"] = list(column_names)
    if filters:
        body["filters"] = [
            f.model_dump(by_alias=True) if isinstance(f, DownloadFilter) else dict(f)
            for f in filters
        ]
    return body or None
