"""Result type for ingest orchestration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IngestResult:
    """Summary of an ingest run (single file or batch directory)."""

    processed: tuple[str, ...]
    skipped: tuple[str, ...]
    pages_written: tuple[str, ...]
    log_appended: bool
