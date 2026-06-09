from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any, Generic, TypeVar

from publicsgdata.datagovsg.models.common import DatasetRow

T = TypeVar("T")


class SyncPageIterator(Generic[T]):
    """Iterate paginated API results synchronously."""

    def __init__(
        self,
        fetch_page: Any,
        *,
        get_items: Any,
        get_next_cursor: Any,
    ) -> None:
        self._fetch_page = fetch_page
        self._get_items = get_items
        self._get_next_cursor = get_next_cursor
        self._cursor: str | None = None
        self._buffer: list[T] = []
        self._index = 0
        self._exhausted = False

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        if self._index >= len(self._buffer):
            if self._exhausted:
                raise StopIteration
            response = self._fetch_page(self._cursor)
            self._buffer = list(self._get_items(response))
            self._index = 0
            self._cursor = self._get_next_cursor(response)
            if not self._buffer:
                self._exhausted = True
                raise StopIteration
            if self._cursor is None:
                self._exhausted = True
        item = self._buffer[self._index]
        self._index += 1
        return item


class AsyncPageIterator(Generic[T]):
    """Iterate paginated API results asynchronously."""

    def __init__(
        self,
        fetch_page: Any,
        *,
        get_items: Any,
        get_next_cursor: Any,
    ) -> None:
        self._fetch_page = fetch_page
        self._get_items = get_items
        self._get_next_cursor = get_next_cursor
        self._cursor: str | None = None
        self._buffer: list[T] = []
        self._index = 0
        self._exhausted = False

    def __aiter__(self) -> AsyncIterator[T]:
        return self

    async def __anext__(self) -> T:
        if self._index >= len(self._buffer):
            if self._exhausted:
                raise StopAsyncIteration
            response = await self._fetch_page(self._cursor)
            self._buffer = list(self._get_items(response))
            self._index = 0
            self._cursor = self._get_next_cursor(response)
            if not self._buffer:
                self._exhausted = True
                raise StopAsyncIteration
            if self._cursor is None:
                self._exhausted = True
        item = self._buffer[self._index]
        self._index += 1
        return item


def parse_cursor_from_next_link(next_link: str | None) -> str | None:
    """Extract cursor query string from v2 list-rows next link."""
    if not next_link:
        return None
    return next_link


def offset_from_ckan_link(next_link: str | None, *, base_path: str) -> int | None:
    """Parse offset from CKAN _links.next relative URL."""
    if not next_link:
        return None
    from urllib.parse import parse_qs, urlparse

    parsed = urlparse(next_link if "://" in next_link else f"{base_path}{next_link}")
    values = parse_qs(parsed.query).get("offset")
    if not values:
        return None
    return int(values[0])


class CkanSearchIterator(SyncPageIterator[DatasetRow]):
    """Sync iterator for CKAN datastore_search offset pagination."""

    def __init__(
        self,
        fetch_page: Any,
        *,
        initial_offset: int = 0,
    ) -> None:
        super().__init__(
            lambda cursor: fetch_page(int(cursor) if cursor is not None else initial_offset),
            get_items=lambda response: response.records,
            get_next_cursor=lambda response: (
                str(response.offset + len(response.records))
                if response.links.next is not None and len(response.records) > 0
                else None
            ),
        )
        if initial_offset:
            self._cursor = str(initial_offset)


class AsyncCkanSearchIterator(AsyncPageIterator[DatasetRow]):
    """Async iterator for CKAN datastore_search offset pagination."""

    def __init__(
        self,
        fetch_page: Any,
        *,
        initial_offset: int = 0,
    ) -> None:
        super().__init__(
            lambda cursor: fetch_page(int(cursor) if cursor is not None else initial_offset),
            get_items=lambda response: response.records,
            get_next_cursor=lambda response: (
                str(response.offset + len(response.records))
                if response.links.next is not None and len(response.records) > 0
                else None
            ),
        )
        if initial_offset:
            self._cursor = str(initial_offset)
