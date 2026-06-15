"""Canned LLM responses for CLI integration and E2E tests (S2-12)."""

from __future__ import annotations

from contract.fakes import InMemoryLLMFake

INGEST_LLM_RESPONSE = """\
## TAKEAWAYS
Summary of the source note.

## WIKI_PAGES
### daily-note.md
Wiki page body from ingest.

## INDEX_UPDATE
- [Daily Note](daily-note.md)
"""

QUERY_LLM_RESPONSE = """\
## ANSWER
Themes include [Daily Note](daily-note.md) and reflection.

## CITATIONS
- daily-note.md
"""

LINT_LLM_RESPONSE = """\
## SUMMARY
No issues found.

## FINDINGS
(none)
"""


def canned_cli_llm() -> InMemoryLLMFake:
    """Return an InMemoryLLMFake with responses for ingest, query, and lint."""
    return InMemoryLLMFake(
        responses={
            "Ingest the following": INGEST_LLM_RESPONSE,
            "Answer the question using only": QUERY_LLM_RESPONSE,
            "Health-check the wiki for contradictions": LINT_LLM_RESPONSE,
        }
    )
