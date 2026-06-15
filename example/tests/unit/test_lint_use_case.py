"""Unit tests for LintUseCase (S9, S13)."""

from __future__ import annotations

from pathlib import Path

from contract.fakes import (
    InMemoryConfigurationFake,
    InMemoryInteractionFake,
    InMemoryLLMFake,
    InMemoryWikiStorageFake,
)
from llm_wiki.domain.prompts.lint import LINT_SCAN_EXCLUDES, lint_log_heading_matches
from llm_wiki.domain.use_cases.lint import LintUseCase

SAMPLE_LLM_RESPONSE = """\
## SUMMARY
1 contradiction, 1 orphan

## FINDINGS
### contradiction | daily-note.md
The page claims morning focus but topics/overview says evening focus.

Suggestion: Reconcile the theme descriptions between pages.

### orphan | orphaned-page.md
Page is not linked from index or other wiki pages.

Suggestion: Add a link in index.md or from a related page.
"""

CLEAN_LLM_RESPONSE = """\
## SUMMARY
No issues found.

## FINDINGS
(none)
"""


def _seed_wiki(storage: InMemoryWikiStorageFake) -> None:
    storage.wiki_pages["SCHEMA.md"] = "# Schema"
    storage.wiki_pages["index.md"] = (
        "# Index\n\n- [Daily Note](daily-note.md)\n- [Topics](topics/overview.md)\n"
    )
    storage.wiki_pages["log.md"] = "# Log\n"
    storage.wiki_pages["daily-note.md"] = "Morning focus themes."
    storage.wiki_pages["topics/overview.md"] = "Evening focus overview."
    storage.wiki_pages["orphaned-page.md"] = "Orphan content."


def _make_lint_use_case(
    storage: InMemoryWikiStorageFake,
    *,
    interaction: InMemoryInteractionFake | None = None,
    llm: InMemoryLLMFake | None = None,
) -> LintUseCase:
    config = InMemoryConfigurationFake(
        vault_root=storage.wiki_dir.parent,
        wiki_dir=storage.wiki_dir,
    )
    return LintUseCase(
        storage=storage,
        llm=llm
        or InMemoryLLMFake(
            responses={"Health-check the wiki for contradictions": SAMPLE_LLM_RESPONSE}
        ),
        interaction=interaction or InMemoryInteractionFake(),
        config=config,
    )


def reads_index_and_pages_s9_A1() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    _seed_wiki(storage)
    use_case = _make_lint_use_case(storage)
    expected_pages = sorted(
        path
        for path in storage.wiki_pages
        if path.endswith(".md") and path not in LINT_SCAN_EXCLUDES
    )

    use_case.execute()

    assert storage.call_log.index("read_index") < storage.call_log.index("list_wiki_pages")
    page_reads = [call for call in storage.call_log if call == "read_wiki_page"]
    assert len(page_reads) == len(expected_pages)
    append_pos = storage.call_log.index("append_log")
    assert all(storage.call_log.index("read_wiki_page") < append_pos for _ in page_reads)


def report_has_suggestions_s9_A2() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    _seed_wiki(storage)
    interaction = InMemoryInteractionFake()
    use_case = _make_lint_use_case(storage, interaction=interaction)

    result = use_case.execute()

    assert len(result.findings) == 2
    assert interaction.presented
    report = interaction.presented[0]
    assert report.count("**Suggestion:**") >= len(result.findings)


def clean_wiki_report_s9_A3() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    _seed_wiki(storage)
    llm = InMemoryLLMFake(
        responses={"Health-check the wiki for contradictions": CLEAN_LLM_RESPONSE}
    )
    use_case = _make_lint_use_case(storage, llm=llm)

    result = use_case.execute()

    assert result.findings == ()
    assert "No issues found" in result.report
    assert result.log_appended is True
    assert len(storage.log_entries) == 1


def no_page_writes_s9_B1() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    _seed_wiki(storage)
    use_case = _make_lint_use_case(storage)

    use_case.execute()

    assert "write_wiki_page" not in storage.call_log
    assert "write_index" not in storage.call_log


def only_log_append_s9_B2() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    _seed_wiki(storage)
    use_case = _make_lint_use_case(storage)

    use_case.execute()

    write_calls = {
        call.split(":", 1)[0]
        for call in storage.call_log
        if call.startswith(("write_", "append_log"))
    }
    assert write_calls == {"append_log"}


def lint_log_heading_s13_C1() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    _seed_wiki(storage)
    use_case = _make_lint_use_case(storage)

    use_case.execute()

    assert storage.log_entries[0].startswith("## [")
    assert " lint | " in storage.log_entries[0]
    assert lint_log_heading_matches(storage.log_entries[0])


def no_autofix_binding_s9_Y1() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    _seed_wiki(storage)
    use_case = _make_lint_use_case(storage)

    use_case.execute()

    assert "write_wiki_page" not in storage.call_log
    assert "write_index" not in storage.call_log
