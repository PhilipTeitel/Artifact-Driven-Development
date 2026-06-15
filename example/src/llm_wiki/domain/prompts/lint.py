"""Lint prompt templates and LLM response parsing."""

from __future__ import annotations

import re

from llm_wiki.domain.models.lint_result import LintFinding

LINT_SCAN_EXCLUDES: frozenset[str] = frozenset({"SCHEMA.md", "log.md", ".ingested.json"})

_LINT_CATEGORIES = (
    "contradiction",
    "stale",
    "orphan",
    "missing_concept",
    "broken_link",
)
_FINDING_HEADER = re.compile(
    r"^###\s+(?P<category>\w+)\s*\|\s*(?P<location>.+)$",
    re.MULTILINE,
)
_SUGGESTION_LINE = re.compile(r"^Suggestion:\s*(.+)$", re.MULTILINE | re.IGNORECASE)
_LINT_LOG_HEADING = re.compile(r"^## \[\d{4}-\d{2}-\d{2}\] lint \|")


def build_lint_prompt(
    *,
    index_content: str,
    page_contents: dict[str, str],
) -> str:
    """Build the lint completion prompt from index and wiki pages."""
    pages_block = "\n\n".join(
        f"### {page_path}\n{content}" for page_path, content in page_contents.items()
    )
    categories = ", ".join(_LINT_CATEGORIES)
    return (
        "Health-check the wiki for contradictions, stale claims, orphan pages, "
        "missing concept pages, and broken cross-references.\n"
        f"Categories: {categories}.\n"
        "Respond with markdown using exactly these labeled sections:\n"
        "## SUMMARY\n"
        "(counts by category or 'No issues found')\n"
        "## FINDINGS\n"
        "(for each issue use a heading `### {category} | {wiki-relative-path}` "
        "followed by description and a line `Suggestion: ...`)\n"
        f"\n## INDEX\n{index_content}\n\n"
        f"## WIKI_PAGES\n{pages_block}"
    )


def parse_lint_response(text: str) -> tuple[LintFinding, ...]:
    """Parse structured lint findings from an LLM response."""
    findings_section = _extract_section(text, "FINDINGS")
    if not findings_section or findings_section.lower() in {"(none)", "none"}:
        return ()

    findings: list[LintFinding] = []
    headers = list(_FINDING_HEADER.finditer(findings_section))
    for index, match in enumerate(headers):
        category = match.group("category").strip().lower()
        location = match.group("location").strip()
        start = match.end()
        end = headers[index + 1].start() if index + 1 < len(headers) else len(findings_section)
        body = findings_section[start:end].strip()
        suggestion_match = _SUGGESTION_LINE.search(body)
        suggestion = suggestion_match.group(1).strip() if suggestion_match else ""
        description = _SUGGESTION_LINE.sub("", body).strip()
        findings.append(
            LintFinding(
                category=category,
                location=location,
                description=description,
                suggestion=suggestion,
            )
        )
    return tuple(findings)


def build_lint_report(
    findings: tuple[LintFinding, ...],
    *,
    summary: str | None = None,
) -> str:
    """Format a human-readable lint report with explicit Suggestion lines."""
    if not findings:
        summary_line = summary or "No issues found."
        return f"# Lint Report\n\n## Summary\n{summary_line}\n\n## Findings\nNo issues found.\n"

    category_counts: dict[str, int] = {}
    for finding in findings:
        category_counts[finding.category] = category_counts.get(finding.category, 0) + 1

    if summary is None:
        parts = [f"{count} {category}" for category, count in sorted(category_counts.items())]
        summary_line = ", ".join(parts)
    else:
        summary_line = summary

    lines = ["# Lint Report", "", "## Summary", summary_line, "", "## Findings"]
    for finding in findings:
        lines.append(f"### {finding.category} | {finding.location}")
        lines.append(finding.description)
        lines.append(f"**Suggestion:** {finding.suggestion}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def extract_lint_summary(text: str) -> str:
    """Return the SUMMARY section body from an LLM response."""
    return _extract_section(text, "SUMMARY") or "Lint complete"


def lint_log_heading_matches(entry: str) -> bool:
    """Return True when the first line matches ADR-003 lint log heading."""
    first_line = entry.splitlines()[0] if entry else ""
    return bool(_LINT_LOG_HEADING.match(first_line))


def lint_log_title(findings: tuple[LintFinding, ...]) -> str:
    """Derive a short log title from lint findings."""
    if not findings:
        return "wiki clean"
    return f"{len(findings)} issue{'s' if len(findings) != 1 else ''} found"


def _extract_section(text: str, name: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(name)}\s*$", re.MULTILINE | re.IGNORECASE)
    match = pattern.search(text)
    if not match:
        return ""
    start = match.end()
    next_header = re.search(r"^##\s+", text[start:], re.MULTILINE)
    end = start + next_header.start() if next_header else len(text)
    return text[start:end].strip()
