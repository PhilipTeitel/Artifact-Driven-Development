"""Ingest prompt templates and deterministic LLM response parsing."""

from __future__ import annotations

import re
from dataclasses import dataclass

_SECTION_HEADER = re.compile(r"^##\s+(.+)$", re.MULTILINE)
_PAGE_HEADER = re.compile(r"^###\s+(.+)$", re.MULTILINE)
_INGEST_LOG_HEADING = re.compile(r"^## \[\d{4}-\d{2}-\d{2}\] ingest \|")


@dataclass(frozen=True)
class IngestParseResult:
    """Structured output parsed from an ingest LLM response."""

    takeaways: str
    wiki_pages: dict[str, str]
    index_update: str


def build_ingest_prompt(*, source_path: str, content: str) -> str:
    """Build the ingest completion prompt for a vault source file."""
    return (
        "Ingest the following vault source into the wiki.\n"
        "Respond with markdown using exactly these labeled sections:\n"
        "## TAKEAWAYS\n"
        "## WIKI_PAGES\n"
        "(use ### filename.md subheadings for each page body)\n"
        "## INDEX_UPDATE\n"
        f"\nSource path: {source_path}\n\n"
        f"{content}"
    )


def parse_ingest_response(text: str) -> IngestParseResult:
    """Parse labeled markdown sections from an ingest LLM response."""
    sections: dict[str, str] = {}
    headers = list(_SECTION_HEADER.finditer(text))
    for index, match in enumerate(headers):
        name = match.group(1).strip().upper()
        start = match.end()
        end = headers[index + 1].start() if index + 1 < len(headers) else len(text)
        sections[name] = text[start:end].strip()

    wiki_pages = _parse_wiki_pages(sections.get("WIKI_PAGES", ""))
    return IngestParseResult(
        takeaways=sections.get("TAKEAWAYS", "").strip(),
        wiki_pages=wiki_pages,
        index_update=sections.get("INDEX_UPDATE", "").strip(),
    )


def _parse_wiki_pages(section_body: str) -> dict[str, str]:
    pages: dict[str, str] = {}
    headers = list(_PAGE_HEADER.finditer(section_body))
    if not headers:
        return pages
    for index, match in enumerate(headers):
        page_path = match.group(1).strip()
        start = match.end()
        end = headers[index + 1].start() if index + 1 < len(headers) else len(section_body)
        pages[page_path] = section_body[start:end].strip()
    return pages


def ingest_log_heading_matches(entry: str) -> bool:
    """Return True when the first line matches ADR-003 ingest log heading."""
    first_line = entry.splitlines()[0] if entry else ""
    return bool(_INGEST_LOG_HEADING.match(first_line))
