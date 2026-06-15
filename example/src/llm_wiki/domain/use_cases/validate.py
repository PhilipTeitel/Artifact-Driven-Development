"""Validate vault wiki layout (S10)."""

from __future__ import annotations

import logging

from llm_wiki.domain.models import ValidationIssue, ValidationResult
from llm_wiki.ports.configuration import ConfigurationPort
from llm_wiki.ports.schema import SchemaPort
from llm_wiki.ports.storage import WikiStoragePort

logger = logging.getLogger("llm_wiki.domain.use_cases")

_REQUIRED_ARTIFACTS: tuple[tuple[str, str, str], ...] = (
    ("SCHEMA.md", "missing_schema", "Missing required file SCHEMA.md"),
    ("index.md", "missing_index", "Missing required file index.md"),
    ("log.md", "missing_log", "Missing required file log.md"),
)


class ValidateUseCase:
    """Check wiki layout and return named validation issues for CLI exit codes."""

    def __init__(
        self,
        *,
        storage: WikiStoragePort,
        schema: SchemaPort,
        config: ConfigurationPort,
    ) -> None:
        self._storage = storage
        self._schema = schema
        self._config = config

    def execute(self) -> ValidationResult:
        """Check vault/wiki layout; return issues for S10."""
        issues: list[ValidationIssue] = []

        if not self._storage.wiki_exists():
            issues.append(
                ValidationIssue(
                    code="missing_wiki",
                    message="Wiki layout is not initialized",
                    path=self._config.wiki_dir,
                )
            )
            logger.info("Validation failed: wiki layout missing")
            return ValidationResult(valid=False, issues=tuple(issues))

        for relative_path, code, message in _REQUIRED_ARTIFACTS:
            if not self._artifact_readable(relative_path):
                issues.append(
                    ValidationIssue(
                        code=code,
                        message=message,
                        path=self._config.wiki_dir / relative_path,
                    )
                )

        valid = len(issues) == 0
        if not valid:
            logger.info("Validation failed with %d issue(s)", len(issues))
        else:
            logger.debug("Validation passed")
        return ValidationResult(valid=valid, issues=tuple(issues))

    def _artifact_readable(self, relative_path: str) -> bool:
        try:
            if relative_path == "index.md":
                self._storage.read_index()
            else:
                self._storage.read_wiki_page(relative_path)
        except (KeyError, OSError):
            return False
        return True
