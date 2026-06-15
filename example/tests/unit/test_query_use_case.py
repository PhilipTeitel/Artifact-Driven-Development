"""Unit tests for QueryUseCase (S8, S13)."""

from __future__ import annotations

from pathlib import Path

from contract.fakes import (
    InMemoryConfigurationFake,
    InMemoryInteractionFake,
    InMemoryLLMFake,
    InMemoryWikiStorageFake,
)
from llm_wiki.domain.prompts.query import query_log_heading_matches
from llm_wiki.domain.use_cases.query import _CONFIRM_MESSAGE, QueryUseCase

SAMPLE_LLM_RESPONSE = """\
## ANSWER
Themes include [Daily Note](daily-note.md) and reflection.

## CITATIONS
- daily-note.md
"""


def _seed_wiki(storage: InMemoryWikiStorageFake) -> None:
    storage.wiki_pages["index.md"] = (
        "# Index\n\n- [Daily Note](daily-note.md)\n- [Topics](topics/overview.md)\n"
    )
    storage.wiki_pages["daily-note.md"] = "Daily reflection themes."
    storage.wiki_pages["topics/overview.md"] = "Overview of topics."


def _make_query_use_case(
    storage: InMemoryWikiStorageFake,
    *,
    interaction: InMemoryInteractionFake | None = None,
    llm: InMemoryLLMFake | None = None,
) -> QueryUseCase:
    config = InMemoryConfigurationFake(
        vault_root=storage.wiki_dir.parent,
        wiki_dir=storage.wiki_dir,
    )
    return QueryUseCase(
        storage=storage,
        llm=llm
        or InMemoryLLMFake(responses={"Answer the question using only": SAMPLE_LLM_RESPONSE}),
        interaction=interaction or InMemoryInteractionFake(),
        config=config,
    )


def index_read_first_s8_A1() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    _seed_wiki(storage)
    use_case = _make_query_use_case(storage)

    use_case.execute("What themes appear in the daily note?")

    index_pos = storage.call_log.index("read_index")
    page_reads = [i for i, call in enumerate(storage.call_log) if call == "read_wiki_page"]
    assert page_reads, "expected at least one wiki page read"
    assert all(index_pos < pos for pos in page_reads)


def answer_has_citations_s8_A2() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    _seed_wiki(storage)
    use_case = _make_query_use_case(storage)

    result = use_case.execute("What themes appear in the daily note?")

    assert "daily-note.md" in result.citations


def presents_before_confirm_s8_A3() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    _seed_wiki(storage)
    timeline: list[str] = []
    interaction = InMemoryInteractionFake(timeline=timeline)
    use_case = _make_query_use_case(storage, interaction=interaction)

    use_case.execute("What themes appear in the daily note?")

    assert len(interaction.presented) == 1
    assert "Daily Note" in interaction.presented[0]
    assert timeline.index("present") < timeline.index("confirm")


def confirm_files_answer_s8_B1() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    _seed_wiki(storage)
    use_case = _make_query_use_case(storage)

    result = use_case.execute("What themes appear in the daily note?")

    assert result.filed is True
    assert result.filed_page is not None
    assert result.filed_page in storage.wiki_pages
    assert "write_index" in storage.call_log
    assert len(storage.log_entries) == 1
    assert query_log_heading_matches(storage.log_entries[0])


def decline_no_writes_s8_B2() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    _seed_wiki(storage)
    interaction = InMemoryInteractionFake(confirm_responses={_CONFIRM_MESSAGE: False})
    use_case = _make_query_use_case(storage, interaction=interaction)

    result = use_case.execute("What themes appear in the daily note?")

    assert result.filed is False
    assert result.filed_page is None
    assert "write_wiki_page" not in storage.call_log
    assert "write_index" not in storage.call_log
    assert "append_log" not in storage.call_log


def query_log_heading_s13_C1() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    _seed_wiki(storage)
    use_case = _make_query_use_case(storage)

    use_case.execute("What themes appear in the daily note?")

    assert storage.log_entries[0].startswith("## [")
    assert " query | " in storage.log_entries[0]
    assert query_log_heading_matches(storage.log_entries[0])


def no_source_reads_s5_D1() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    _seed_wiki(storage)
    use_case = _make_query_use_case(storage)

    use_case.execute("What themes appear in the daily note?")

    assert "read_source" not in storage.call_log


def index_first_binding_s8_Y1() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    _seed_wiki(storage)
    use_case = _make_query_use_case(storage)

    use_case.execute("What themes appear in the daily note?")

    if "read_wiki_page" in storage.call_log:
        assert storage.call_log.index("read_index") < storage.call_log.index("read_wiki_page")


def filing_gate_binding_s8_Y2() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    _seed_wiki(storage)
    interaction = InMemoryInteractionFake(confirm_responses={_CONFIRM_MESSAGE: False})
    use_case = _make_query_use_case(storage, interaction=interaction)

    use_case.execute("What themes appear in the daily note?")

    write_calls = {"write_wiki_page", "write_index", "append_log"}
    assert not any(call.split(":", 1)[0] in write_calls for call in storage.call_log)
