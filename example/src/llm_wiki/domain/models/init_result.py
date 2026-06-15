"""Init layout outcome model."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class InitResult:
    """Outcome of idempotent wiki layout initialization (S1, S2)."""

    created: tuple[str, ...]
    already_present: tuple[str, ...]
    wiki_dir: Path
