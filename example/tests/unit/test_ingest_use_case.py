"""Unit tests for IngestUseCase (S6, S7, S12, S13)."""

from __future__ import annotations

import re
from pathlib import Path

from contract.fakes import (
    InMemoryConfigurationFake,
    InMemoryInteractionFake,
    InMemoryLLMFake,
    InMemorySchemaFake,
    InMemoryWikiStorageFake,
)
from llm_wiki.domain.prompts.ingest import ingest_log_heading_matches
from llm_wiki.domain.use_cases.ingest import _CONFIRM_MESSAGE, IngestUseCase

ISO_UTC_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

SAMPLE_LLM_RESPONSE = """\
## TAKEAWAYS
Summary of the source note.

## WIKI_PAGES
### daily-note.md
Wiki page body.

## INDEX_UPDATE
- [Daily Note](daily-note.md)
"""


def _make_ingest_use_case(
    storage: InMemoryWikiStorageFake,
    *,
    batch_mode: bool = False,
    interaction: InMemoryInteractionFake | None = None,
    llm: InMemoryLLMFake | None = None,
    schema: InMemorySchemaFake | None = None,
) -> IngestUseCase:
    config = InMemoryConfigurationFake(
        vault_root=storage.wiki_dir.parent,
        wiki_dir=storage.wiki_dir,
        batch_mode=batch_mode,
    )
    return IngestUseCase(
        storage=storage,
        llm=llm or InMemoryLLMFake(responses={"Ingest the following": SAMPLE_LLM_RESPONSE}),
        schema=schema or InMemorySchemaFake(),
        interaction=interaction or InMemoryInteractionFake(),
        config=config,
    )


def _seed_single_source(storage: InMemoryWikiStorageFake, path: str = "daily/note.md") -> str:
    storage.sources[path] = "# Source content"
    storage.wiki_pages["index.md"] = "# Index"
    return path


def interactive_presents_before_write_s6_A1() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    source = _seed_single_source(storage)
    timeline: list[str] = []
    interaction = InMemoryInteractionFake(timeline=timeline)
    use_case = _make_ingest_use_case(storage, interaction=interaction)

    use_case.execute(source)

    write_index = next(
        (
            index
            for index, call in enumerate(storage.call_log)
            if call.startswith("write_wiki_page")
        ),
        None,
    )
    assert "read_source" in storage.call_log
    assert len(interaction.presented) == 1
    assert interaction.presented[0] == "Summary of the source note."
    assert "present" in timeline
    assert write_index is not None
    assert timeline.index("present") < storage.call_log.index(
        next(call for call in storage.call_log if call.startswith("write_wiki_page"))
    )


def confirm_writes_wiki_artifacts_s6_A2() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    source = _seed_single_source(storage)
    use_case = _make_ingest_use_case(storage)

    result = use_case.execute(source)

    assert result.processed == (source,)
    assert "daily-note.md" in result.pages_written
    assert storage.wiki_pages["daily-note.md"] == "Wiki page body."
    assert storage.index_content == "- [Daily Note](daily-note.md)"
    assert len(storage.log_entries) == 1
    assert ingest_log_heading_matches(storage.log_entries[0])
    assert source in storage.ingested["sources"]
    assert ISO_UTC_PATTERN.match(storage.ingested["sources"][source])
    assert result.log_appended is True


def decline_skips_writes_s6_A3() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    source = _seed_single_source(storage)
    interaction = InMemoryInteractionFake(confirm_responses={_CONFIRM_MESSAGE: False})
    use_case = _make_ingest_use_case(storage, interaction=interaction)

    result = use_case.execute(source)

    assert result.processed == ()
    assert "write_wiki_page" not in storage.call_log
    assert "write_index" not in storage.call_log
    assert "append_log" not in storage.call_log
    assert "write_ingested" not in storage.call_log


def batch_no_confirm_s7_B1() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    storage.sources["batch/a.md"] = "# A"
    storage.sources["batch/b.md"] = "# B"
    storage.wiki_pages["index.md"] = "# Index"
    interaction = InMemoryInteractionFake()
    use_case = _make_ingest_use_case(storage, batch_mode=True, interaction=interaction)

    use_case.execute("batch/")

    assert interaction.presented == []
    assert storage.call_log.count("read_source") == 2
    assert any(call.startswith("write_wiki_page") for call in storage.call_log)


def batch_skips_excludes_s7_B2() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    storage.sources["batch/ok.md"] = "# OK"
    storage.sources["batch/drafts/hidden.md"] = "# Hidden"
    storage.wiki_pages["index.md"] = "# Index"
    schema = InMemorySchemaFake(excludes=(".obsidian/", "wiki/", ".*", "batch/drafts/"))
    use_case = _make_ingest_use_case(storage, batch_mode=True, schema=schema)

    result = use_case.execute("batch/")

    assert "batch/drafts/hidden.md" in result.skipped
    assert "batch/ok.md" in result.processed


def batch_each_file_logged_s7_B3() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    storage.sources["batch/a.md"] = "# A"
    storage.sources["batch/b.md"] = "# B"
    storage.wiki_pages["index.md"] = "# Index"
    use_case = _make_ingest_use_case(storage, batch_mode=True)

    result = use_case.execute("batch/")

    assert len(result.processed) == 2
    assert len(storage.log_entries) == 2
    assert all(ingest_log_heading_matches(entry) for entry in storage.log_entries)
    assert result.log_appended is True


def ingested_sidecar_updated_s12_C1() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    source = _seed_single_source(storage)
    use_case = _make_ingest_use_case(storage)

    use_case.execute(source)

    assert storage.ingested["version"] == 1
    assert ISO_UTC_PATTERN.match(storage.ingested["sources"][source])


def batch_skips_ingested_s12_C2() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    storage.sources["batch/a.md"] = "# A"
    storage.sources["batch/b.md"] = "# B"
    storage.wiki_pages["index.md"] = "# Index"
    storage.ingested = {
        "version": 1,
        "sources": {"batch/a.md": "2026-01-01T00:00:00Z"},
    }
    use_case = _make_ingest_use_case(storage, batch_mode=True)

    result = use_case.execute("batch/")

    assert "batch/a.md" in result.skipped
    assert "batch/b.md" in result.processed
    assert storage.ingested_writes == 1


def ingest_log_heading_s13_D1() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    source = _seed_single_source(storage, "topics/my-topic.md")
    use_case = _make_ingest_use_case(storage)

    use_case.execute(source)

    assert ingest_log_heading_matches(storage.log_entries[0])
    assert storage.log_entries[0].startswith("## [")
    assert " ingest | " in storage.log_entries[0]


def no_source_writes_s5_D2() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    source = _seed_single_source(storage)
    use_case = _make_ingest_use_case(storage)

    use_case.execute(source)

    assert "read_source" in storage.call_log
    wiki_writes = [call for call in storage.call_log if call.startswith("write_wiki_page:")]
    assert all(not call.endswith(f":{source}") for call in wiki_writes)
    assert source not in storage.wiki_pages


def batch_mode_from_config_s19_E2() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    source = _seed_single_source(storage)
    interaction = InMemoryInteractionFake()
    use_case = _make_ingest_use_case(storage, batch_mode=True, interaction=interaction)

    use_case.execute(source)

    assert interaction.presented == []
    assert any(call.startswith("write_wiki_page") for call in storage.call_log)


def ingest_port_only_s16_Y1() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    source = _seed_single_source(storage)
    use_case = _make_ingest_use_case(storage)

    use_case.execute(source)

    port_methods = {
        "read_source",
        "read_ingested",
        "write_wiki_page",
        "write_index",
        "append_log",
        "write_ingested",
        "list_sources",
    }
    for call in storage.call_log:
        method = call.split(":", 1)[0]
        assert method in port_methods or method == "read_ingested"


def ingested_shape_binding_s12_Y2() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    source = _seed_single_source(storage)
    use_case = _make_ingest_use_case(storage)

    use_case.execute(source)

    sidecar = storage.ingested
    assert sidecar["version"] == 1
    assert isinstance(sidecar["sources"], dict)
    assert all(isinstance(value, str) for value in sidecar["sources"].values())


def interactive_gate_binding_s6_Y3() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    source = _seed_single_source(storage)
    interaction = InMemoryInteractionFake(confirm_responses={_CONFIRM_MESSAGE: False})
    use_case = _make_ingest_use_case(storage, interaction=interaction)

    use_case.execute(source)

    assert "write_wiki_page" not in storage.call_log


def skip_ingested_binding_s12_Y4() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    storage.sources["batch/only.md"] = "# Only"
    storage.wiki_pages["index.md"] = "# Index"
    storage.ingested = {
        "version": 1,
        "sources": {"batch/only.md": "2026-01-01T00:00:00Z"},
    }
    use_case = _make_ingest_use_case(storage, batch_mode=True)

    result = use_case.execute("batch/")

    assert result.processed == ()
    assert result.skipped == ("batch/only.md",)
    assert "write_wiki_page" not in storage.call_log
