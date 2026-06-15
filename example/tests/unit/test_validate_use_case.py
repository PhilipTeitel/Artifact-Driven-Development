"""Unit tests for ValidateUseCase (S10)."""

from __future__ import annotations

from pathlib import Path

from contract.fakes import (
    REQUIRED_WIKI_ARTIFACTS,
    InMemoryConfigurationFake,
    InMemorySchemaFake,
    InMemoryWikiStorageFake,
)
from llm_wiki.domain.use_cases.validate import ValidateUseCase


def _make_validate_use_case(storage: InMemoryWikiStorageFake) -> ValidateUseCase:
    config = InMemoryConfigurationFake(
        vault_root=storage.wiki_dir.parent,
        wiki_dir=storage.wiki_dir,
    )
    return ValidateUseCase(
        storage=storage,
        schema=InMemorySchemaFake(),
        config=config,
    )


def _seed_complete_layout(storage: InMemoryWikiStorageFake) -> None:
    for artifact in REQUIRED_WIKI_ARTIFACTS:
        storage.wiki_pages[artifact] = f"content-{artifact}"
    storage._layout_initialized = True


def valid_layout_s10_D1() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    _seed_complete_layout(storage)
    use_case = _make_validate_use_case(storage)

    result = use_case.execute()

    assert result.valid is True
    assert result.issues == ()


def missing_schema_s10_D2() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    storage.wiki_pages["index.md"] = "index"
    storage.wiki_pages["log.md"] = "log"
    storage._layout_initialized = True
    use_case = _make_validate_use_case(storage)

    result = use_case.execute()

    assert result.valid is False
    codes = {issue.code for issue in result.issues}
    assert "missing_schema" in codes
    schema_issue = next(i for i in result.issues if i.code == "missing_schema")
    assert "SCHEMA" in schema_issue.message


def multiple_issues_named_s10_D3() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    storage.wiki_pages["SCHEMA.md"] = "schema"
    storage._layout_initialized = True
    use_case = _make_validate_use_case(storage)

    result = use_case.execute()

    assert result.valid is False
    codes = {issue.code for issue in result.issues}
    assert codes == {"missing_index", "missing_log"}
    messages = " ".join(issue.message for issue in result.issues)
    assert "index.md" in messages
    assert "log.md" in messages


def no_wiki_dir_s10_D4() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    use_case = _make_validate_use_case(storage)

    result = use_case.execute()

    assert result.valid is False
    assert len(result.issues) == 1
    assert result.issues[0].code == "missing_wiki"
    assert "wiki" in result.issues[0].message.lower()


def validate_binding_s10_Y4() -> None:
    storage = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    use_case = _make_validate_use_case(storage)

    result = use_case.execute()

    assert result.valid is False
    for issue in result.issues:
        assert issue.code
        assert issue.message
