"""Parse Excludes bullets from wiki/SCHEMA.md (ADR-003)."""

from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)

_EXCLUDES_HEADING = re.compile(r"^##\s+Excludes\s*$", re.MULTILINE)
_NEXT_SECTION = re.compile(r"^##\s+", re.MULTILINE)
_BULLET = re.compile(r"^\s*[-*]\s+(.+)$", re.MULTILINE)
_BACKTICKS = re.compile(r"`([^`]+)`")
_TRAILING_COMMENT = re.compile(r"\s+(?:—|--|-)\s+.*$")


def extract_excludes_section(content: str) -> str | None:
    """Return markdown body of the Excludes section, or None if missing."""
    match = _EXCLUDES_HEADING.search(content)
    if match is None:
        return None
    start = match.end()
    rest = content[start:]
    next_heading = _NEXT_SECTION.search(rest)
    body = rest[: next_heading.start()] if next_heading else rest
    return body.strip()


def parse_exclude_bullets(section_body: str) -> list[str]:
    """Parse glob patterns from Excludes section bullet lines."""
    patterns: list[str] = []
    for match in _BULLET.finditer(section_body):
        raw = match.group(1).strip()
        if not raw or raw.startswith("<!--"):
            continue
        cleaned = _BACKTICKS.sub(r"\1", raw)
        cleaned = _TRAILING_COMMENT.sub("", cleaned).strip()
        if cleaned:
            patterns.append(cleaned)
    return patterns


def parse_excludes_from_schema(content: str) -> list[str] | None:
    """Parse exclude patterns from full SCHEMA.md content."""
    section = extract_excludes_section(content)
    if section is None:
        logger.warning("SCHEMA.md missing Excludes section; using default excludes")
        return None
    patterns = parse_exclude_bullets(section)
    if not patterns:
        logger.warning("SCHEMA.md Excludes section has no bullets; using default excludes")
        return None
    return patterns
