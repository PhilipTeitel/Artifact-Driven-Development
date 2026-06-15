"""Wiki schema and ingest sidecar models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

WikiOperation = Literal["init", "ingest", "query", "lint"]


@dataclass(frozen=True)
class WikiSchema:
    """Parsed SCHEMA.md subset (S4) — full parse in S2-4 adapter."""

    excludes: tuple[str, ...]
    raw_sections: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class IngestedSidecar:
    """wiki/.ingested.json document (ADR-003)."""

    version: int
    sources: dict[str, str]
