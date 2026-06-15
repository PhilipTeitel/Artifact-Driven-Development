"""Validation outcome models (S10)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class ValidationIssue:
    """Single validation finding (S10)."""

    code: str
    message: str
    path: Path | None = None


@dataclass(frozen=True)
class ValidationResult:
    """Aggregate validate outcome (S10)."""

    valid: bool
    issues: tuple[ValidationIssue, ...] = field(default_factory=tuple)
