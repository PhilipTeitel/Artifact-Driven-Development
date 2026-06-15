"""Markdown SCHEMA.md parser adapter (S2-4)."""

from __future__ import annotations

import logging
import re
from pathlib import Path

from llm_wiki.adapters.schema.excludes_parser import parse_excludes_from_schema
from llm_wiki.domain.models import WikiSchema
from llm_wiki.ports.configuration import ConfigurationPort

logger = logging.getLogger(__name__)

_SECTION_HEADING = re.compile(r"^##\s+(.+)$", re.MULTILINE)


class MarkdownSchemaAdapter:
    """Parse wiki/SCHEMA.md for excludes and documented conventions."""

    def __init__(self, *, config: ConfigurationPort) -> None:
        self._config = config

    @property
    def _schema_path(self) -> Path:
        return self._config.wiki_dir / "SCHEMA.md"

    def default_excludes(self) -> list[str]:
        """Used when SCHEMA missing during init template seed."""
        wiki_name = self._config.wiki_dir.name
        wiki_prefix = f"{wiki_name}/" if wiki_name else "wiki/"
        return [".obsidian/", wiki_prefix, ".*"]

    def load(self) -> WikiSchema:
        """Parsed excludes and workflow docs from disk."""
        path = self._schema_path
        if not path.is_file():
            logger.warning("SCHEMA.md not found at %s; using default excludes", path)
            excludes = tuple(self.default_excludes())
            return WikiSchema(excludes=excludes, raw_sections={})

        content = path.read_text(encoding="utf-8")
        raw_sections = self._split_sections(content)
        parsed = parse_excludes_from_schema(content)
        excludes = tuple(parsed if parsed is not None else self.default_excludes())
        return WikiSchema(excludes=excludes, raw_sections=raw_sections)

    def _split_sections(self, content: str) -> dict[str, str]:
        matches = list(_SECTION_HEADING.finditer(content))
        sections: dict[str, str] = {}
        for index, match in enumerate(matches):
            title = match.group(1).strip()
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
            sections[title] = content[start:end].strip()
        return sections
