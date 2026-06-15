"""Contract tests for SchemaPort."""

from __future__ import annotations

from pathlib import Path

from llm_wiki.domain.models import WikiSchema
from llm_wiki.ports.schema import SchemaPort

from .conftest import _markdown_schema_adapter
from .fakes import DEFAULT_EXCLUDES, InMemorySchemaFake


def _run_schema_core_contract(adapter: SchemaPort) -> None:
    """Shared behavioral suite for fake and markdown adapters."""
    assert isinstance(adapter, SchemaPort)
    schema = adapter.load()
    assert isinstance(schema, WikiSchema)
    assert ".obsidian/" in schema.excludes
    assert "wiki/" in schema.excludes
    assert ".*" in schema.excludes
    defaults = adapter.default_excludes()
    for pattern in (".obsidian/", "wiki/", ".*"):
        assert pattern in defaults


def schema_methods_A4() -> None:
    """SchemaPort defines load and default_excludes."""
    assert hasattr(SchemaPort, "load")
    assert hasattr(SchemaPort, "default_excludes")


def schema_core_contract_A1(schema_adapter_impl: SchemaPort) -> None:
    """A1 — core schema contract runs against parametrized fake and markdown adapters."""
    _run_schema_core_contract(schema_adapter_impl)


def default_excludes_s4_C3() -> None:
    """default_excludes includes ADR-003 defaults."""
    fake = InMemorySchemaFake()
    excludes = fake.default_excludes()
    for pattern in (".obsidian/", "wiki/", ".*"):
        assert pattern in excludes


def schema_contract_s4_Y4() -> None:
    """Reference fake satisfies SchemaPort with ADR-003 defaults."""
    fake = InMemorySchemaFake()
    assert isinstance(fake, SchemaPort)
    schema = fake.load()
    assert isinstance(schema, WikiSchema)
    assert set(schema.excludes) == set(DEFAULT_EXCLUDES)


def markdown_adapter_passes_contract_G2(tmp_path: Path) -> None:
    """G2 — MarkdownSchemaAdapter satisfies SchemaPort contract."""
    adapter = _markdown_schema_adapter(tmp_path)
    _run_schema_core_contract(adapter)
