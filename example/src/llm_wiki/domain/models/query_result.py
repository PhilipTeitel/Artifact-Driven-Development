"""Result type for query orchestration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QueryResult:
    """Summary of a query run including optional filing outcome."""

    answer: str
    citations: tuple[str, ...]
    filed: bool
    filed_page: str | None
