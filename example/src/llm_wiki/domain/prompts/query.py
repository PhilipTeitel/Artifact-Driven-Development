"""Query prompt templates, page selection, and LLM response parsing."""

from __future__ import annotations

import re
from dataclasses import dataclass

_SECTION_HEADER = re.compile(r"^##\s+(.+)$", re.MULTILINE)
_INDEX_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_QUERY_LOG_HEADING = re.compile(r"^## \[\d{4}-\d{2}-\d{2}\] query \|")
_CITATION_LINE = re.compile(r"^[-*]\s+(.+)$", re.MULTILINE)


@dataclass(frozen=True)
class QueryParseResult:
    """Structured output parsed from a query LLM response."""

    answer: str
    citations: tuple[str, ...]


def select_pages_from_index(index_content: str, question: str) -> tuple[str, ...]:
    """Select wiki page paths from index links using question keyword overlap."""
    links = _parse_index_links(index_content)
    if not links:
        return ()

    question_tokens = set(re.findall(r"\w+", question.lower()))
    scored: list[tuple[int, str]] = []
    for title, path in links:
        haystack = f"{title} {path}".lower()
        score = sum(1 for token in question_tokens if token in haystack)
        scored.append((score, path))

    scored.sort(key=lambda item: (-item[0], item[1]))
    if any(score > 0 for score, _ in scored):
        return tuple(path for score, path in scored if score > 0)
    return tuple(path for _, path in scored)


def build_query_prompt(
    *,
    question: str,
    index_content: str,
    page_contents: dict[str, str],
) -> str:
    """Build the query completion prompt from index and selected wiki pages."""
    pages_block = "\n\n".join(
        f"### {page_path}\n{content}" for page_path, content in page_contents.items()
    )
    return (
        "Answer the question using only the wiki index and pages below.\n"
        "Respond with markdown using exactly these labeled sections:\n"
        "## ANSWER\n"
        "(include markdown links to cited wiki pages)\n"
        "## CITATIONS\n"
        "(bullet list of wiki-relative page paths you used)\n"
        f"\nQuestion: {question}\n\n"
        "## INDEX\n"
        f"{index_content}\n\n"
        "## WIKI_PAGES\n"
        f"{pages_block}"
    )


def parse_query_response(text: str, *, pages_read: set[str]) -> QueryParseResult:
    """Parse labeled markdown sections and validate citations against pages read."""
    sections: dict[str, str] = {}
    headers = list(_SECTION_HEADER.finditer(text))
    for index, match in enumerate(headers):
        name = match.group(1).strip().upper()
        start = match.end()
        end = headers[index + 1].start() if index + 1 < len(headers) else len(text)
        sections[name] = text[start:end].strip()

    answer = sections.get("ANSWER", "").strip()
    citations_section = sections.get("CITATIONS", "")
    cited_paths = _parse_citation_paths(citations_section, answer)
    validated = tuple(path for path in cited_paths if path in pages_read)
    return QueryParseResult(answer=answer, citations=validated)


def query_log_heading_matches(entry: str) -> bool:
    """Return True when the first line matches ADR-003 query log heading."""
    first_line = entry.splitlines()[0] if entry else ""
    return bool(_QUERY_LOG_HEADING.match(first_line))


def _parse_index_links(index_content: str) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    for match in _INDEX_LINK.finditer(index_content):
        title = match.group(1).strip()
        path = match.group(2).strip()
        if path.endswith(".md"):
            links.append((title, path))
    return links


def _parse_citation_paths(citations_section: str, answer: str) -> tuple[str, ...]:
    paths: list[str] = []
    for match in _CITATION_LINE.finditer(citations_section):
        path = match.group(1).strip()
        if path.endswith(".md"):
            paths.append(path)
    for match in _INDEX_LINK.finditer(answer):
        path = match.group(2).strip()
        if path.endswith(".md") and path not in paths:
            paths.append(path)
    return tuple(paths)
