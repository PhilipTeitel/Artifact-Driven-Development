"""Unit tests for InitUseCase (S1, S2, S13)."""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

from contract.fakes import (
    REQUIRED_WIKI_ARTIFACTS,
    InMemoryConfigurationFake,
    InMemoryInteractionFake,
    InMemoryWikiStorageFake,
)
from llm_wiki.domain.use_cases.init import InitUseCase, init_log_heading_matches


def _make_init_use_case(
    storage: InMemoryWikiStorageFake,
    interaction: InMemoryInteractionFake | None = None,
) -> InitUseCase:
    config = InMemoryConfigurationFake(
        vault_root=storage.wiki_dir.parent,
        wiki_dir=storage.wiki_dir,
    )
    return InitUseCase(
        storage=storage,
        interaction=interaction or InMemoryInteractionFake(),
        config=config,
    )


def fresh_init_creates_layout_s1_A1() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    use_case = _make_init_use_case(storage)

    result = use_case.execute()

    assert set(result.created) == set(REQUIRED_WIKI_ARTIFACTS)
    assert result.already_present == ()
    assert result.wiki_dir == Path("/vault/wiki")


def appends_init_log_s13_A2() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    use_case = _make_init_use_case(storage)

    use_case.execute()

    assert len(storage.log_entries) == 1
    assert init_log_heading_matches(storage.log_entries[0])


def presents_created_summary_s1_A3() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    interaction = InMemoryInteractionFake()
    use_case = _make_init_use_case(storage, interaction=interaction)

    use_case.execute()

    assert len(interaction.presented) == 1
    summary = interaction.presented[0]
    assert "Created:" in summary
    for artifact in REQUIRED_WIKI_ARTIFACTS:
        assert artifact in summary


def idempotent_skips_existing_s2_B1() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    for artifact in REQUIRED_WIKI_ARTIFACTS:
        storage.wiki_pages[artifact] = f"existing-{artifact}"
    storage._layout_initialized = True
    use_case = _make_init_use_case(storage)

    result = use_case.execute()

    assert result.created == ()
    assert set(result.already_present) == set(REQUIRED_WIKI_ARTIFACTS)
    assert storage.call_log.count("ensure_wiki_layout") == 1
    for artifact in REQUIRED_WIKI_ARTIFACTS:
        assert storage.wiki_pages[artifact] == f"existing-{artifact}"


def partial_init_creates_missing_s2_B2() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    storage.wiki_pages["SCHEMA.md"] = "# schema"
    use_case = _make_init_use_case(storage)

    result = use_case.execute()

    assert set(result.created) == {"index.md", "log.md"}
    assert result.already_present == ("SCHEMA.md",)


def no_overwrite_wiki_pages_s2_B3() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    storage.wiki_pages["SCHEMA.md"] = "keep-me"
    storage.wiki_pages["index.md"] = "keep-index"
    storage.wiki_pages["log.md"] = "keep-log"
    storage._layout_initialized = True
    use_case = _make_init_use_case(storage)

    use_case.execute()

    assert storage.wiki_pages["SCHEMA.md"] == "keep-me"
    assert storage.wiki_pages["index.md"] == "keep-index"
    assert storage.wiki_pages["log.md"] == "keep-log"
    assert "write_wiki_page" not in storage.call_log


def no_ingested_sidecar_at_init_C1() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    use_case = _make_init_use_case(storage)

    use_case.execute()

    assert storage.ingested_writes == 0
    assert "write_ingested" not in storage.call_log


def init_port_only_s16_Y1() -> None:
    module_path = Path(inspect.getfile(InitUseCase)).resolve()
    tree = ast.parse(module_path.read_text(encoding="utf-8"))
    imported: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.append(node.module)
    forbidden = ("llm_wiki.adapters", "os", "httpx", "typer")
    violations = [
        name
        for name in imported
        if any(name == prefix or name.startswith(f"{prefix}.") for prefix in forbidden)
    ]
    assert violations == [], f"forbidden imports in init use case: {violations}"


def idempotent_binding_s2_Y2() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    storage.wiki_pages["SCHEMA.md"] = "schema"
    use_case = _make_init_use_case(storage)

    result = use_case.execute()

    assert storage.call_log.count("ensure_wiki_layout") == 1
    assert "SCHEMA.md" in result.already_present
    assert "index.md" in result.created


def log_format_binding_s13_Y3() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    use_case = _make_init_use_case(storage)

    use_case.execute()

    assert init_log_heading_matches(storage.log_entries[0])
