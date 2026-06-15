"""Schema parsing port (ADR-002)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from llm_wiki.domain.models import WikiSchema


@runtime_checkable
class SchemaPort(Protocol):
    """Parse wiki/SCHEMA.md for excludes and documented conventions."""

    def load(self) -> WikiSchema:
        """Parsed excludes and workflow docs."""

    def default_excludes(self) -> list[str]:
        """Used when SCHEMA missing during init template seed."""
