"""Result types for lint orchestration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LintFinding:
    """Single lint issue with a suggested fix."""

    category: str
    location: str
    description: str
    suggestion: str


@dataclass(frozen=True)
class LintResult:
    """Summary of a lint run including report text and log outcome."""

    findings: tuple[LintFinding, ...]
    report: str
    log_appended: bool
