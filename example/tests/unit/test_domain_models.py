"""Unit tests for domain models."""

from __future__ import annotations

from pathlib import Path

from llm_wiki.domain.models import (
    IngestedSidecar,
    ValidationIssue,
    ValidationResult,
    WikiSchema,
)


def validation_models_B2() -> None:
    """ValidationResult and ValidationIssue support S10-style named failures."""
    issue = ValidationIssue(
        code="missing_schema",
        message="SCHEMA.md not found",
        path=Path("wiki/SCHEMA.md"),
    )
    result = ValidationResult(valid=False, issues=(issue,))
    assert result.valid is False
    assert result.issues[0].code == "missing_schema"
    assert result.issues[0].path == Path("wiki/SCHEMA.md")


def wiki_schema_and_sidecar_B3() -> None:
    """WikiSchema and IngestedSidecar align with ADR-003."""
    schema = WikiSchema(excludes=(".obsidian/", "wiki/", ".*"))
    assert ".obsidian/" in schema.excludes
    sidecar = IngestedSidecar(
        version=1,
        sources={"notes/article.md": "2026-05-30T14:22:00Z"},
    )
    assert sidecar.version == 1
    assert sidecar.sources["notes/article.md"] == "2026-05-30T14:22:00Z"