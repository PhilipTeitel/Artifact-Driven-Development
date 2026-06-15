"""Wiki and vault storage port (ADR-002, ADR-003)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from llm_wiki.domain.models import InitResult


@runtime_checkable
class WikiStoragePort(Protocol):
    """All filesystem effects on vault and wiki.

    Non-wiki vault paths are read-only; this port must not expose write/delete
    to paths outside the wiki subdirectory (S5).
    """

    def read_source(self, relative_path: str) -> str:
        """Read-only vault markdown outside wiki."""

    def list_sources(self) -> list[str]:
        """Markdown paths respecting excludes."""

    def read_wiki_page(self, relative_path: str) -> str:
        """Path relative to wiki root."""

    def write_wiki_page(self, relative_path: str, content: str) -> None:
        """Create or update wiki pages."""

    def read_index(self) -> str:
        """Read index.md."""

    def list_wiki_pages(self) -> list[str]:
        """Wiki-relative .md paths for lint/query scans (excludes sidecar artifacts)."""

    def write_index(self, content: str) -> None:
        """Write index.md."""

    def append_log(self, entry: str) -> None:
        """Append-only log.md."""

    def read_ingested(self) -> dict:
        """Read .ingested.json sidecar (ADR-003)."""

    def write_ingested(self, data: dict) -> None:
        """Write .ingested.json sidecar."""

    def wiki_exists(self) -> bool:
        """Init/idempotency checks."""

    def ensure_wiki_layout(self) -> InitResult:
        """Create missing init artifacts (idempotent)."""
