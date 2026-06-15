"""Contract tests for WikiStoragePort."""

from __future__ import annotations

from pathlib import Path
from typing import get_type_hints

from llm_wiki.domain.models import InitResult
from llm_wiki.ports.storage import WikiStoragePort

from .conftest import _filesystem_storage_adapter
from .fakes import REQUIRED_WIKI_ARTIFACTS, InMemoryWikiStorageFake

STORAGE_METHODS = (
    "read_source",
    "list_sources",
    "read_wiki_page",
    "write_wiki_page",
    "read_index",
    "list_wiki_pages",
    "write_index",
    "append_log",
    "read_ingested",
    "write_ingested",
    "wiki_exists",
    "ensure_wiki_layout",
)


def _run_storage_core_contract(adapter: WikiStoragePort) -> None:
    """Shared behavioral suite for fake and filesystem adapters."""
    assert isinstance(adapter, WikiStoragePort)
    result = adapter.ensure_wiki_layout()
    assert isinstance(result, InitResult)
    assert set(result.created) == set(REQUIRED_WIKI_ARTIFACTS)
    second = adapter.ensure_wiki_layout()
    assert second.created == ()
    assert set(second.already_present) == set(REQUIRED_WIKI_ARTIFACTS)
    adapter.write_wiki_page("page.md", "content")
    assert adapter.read_wiki_page("page.md") == "content"
    adapter.append_log("entry")
    adapter.write_ingested({"version": 1, "sources": {"daily/note.md": "2026-01-01T00:00:00Z"}})
    assert adapter.read_ingested()["version"] == 1
    assert adapter.wiki_exists() is True


def storage_methods_A3() -> None:
    """WikiStoragePort defines all ADR-002 methods."""
    for name in STORAGE_METHODS:
        assert hasattr(WikiStoragePort, name)
    hints = get_type_hints(WikiStoragePort.ensure_wiki_layout)
    assert hints["return"] is InitResult
    doc = WikiStoragePort.__doc__ or ""
    assert "non-wiki" in doc.lower() or "outside" in doc.lower()


def storage_core_contract_A1(storage_adapter_impl: WikiStoragePort) -> None:
    """A1 — core storage contract runs against parametrized fake and filesystem adapters."""
    _run_storage_core_contract(storage_adapter_impl)


def init_result_shape_B1() -> None:
    """InitResult captures created, already_present, wiki_dir."""
    fake = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    result = fake.ensure_wiki_layout()
    assert isinstance(result, InitResult)
    assert result.wiki_dir == Path("/vault/wiki")
    assert set(result.created) == set(REQUIRED_WIKI_ARTIFACTS)
    assert result.already_present == ()


def idempotent_layout_s2_C1() -> None:
    """Second ensure_wiki_layout reports already_present without duplicating."""
    fake = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    first = fake.ensure_wiki_layout()
    assert len(first.created) == len(REQUIRED_WIKI_ARTIFACTS)
    second = fake.ensure_wiki_layout()
    assert second.created == ()
    assert set(second.already_present) == set(REQUIRED_WIKI_ARTIFACTS)
    assert len(fake.wiki_pages) == len(REQUIRED_WIKI_ARTIFACTS)


def storage_contract_s2_Y3() -> None:
    """Reference fake satisfies WikiStoragePort including idempotent layout."""
    fake = InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    assert isinstance(fake, WikiStoragePort)
    fake.write_wiki_page("page.md", "content")
    assert fake.read_wiki_page("page.md") == "content"
    fake.append_log("entry")
    assert fake.log_entries == ["entry"]
    fake.write_ingested({"version": 1, "sources": {"a.md": "2026-01-01T00:00:00Z"}})
    assert fake.read_ingested()["version"] == 1
    assert fake.wiki_exists() is False
    fake.ensure_wiki_layout()
    assert fake.wiki_exists() is True


def filesystem_adapter_passes_contract_G1(tmp_path: Path) -> None:
    """G1 — FilesystemWikiStorageAdapter satisfies WikiStoragePort contract."""
    adapter = _filesystem_storage_adapter(tmp_path)
    _run_storage_core_contract(adapter)


def filesystem_adapter_passes_contract_Y5(tmp_path: Path) -> None:
    """Y5 — binding: storage contract suite passes against filesystem adapter."""
    filesystem_adapter_passes_contract_G1(tmp_path)


def filesystem_parametrize_Y2(tmp_path: Path) -> None:
    """Y2 — binding: parametrized filesystem adapter passes storage core contract."""
    adapter = _filesystem_storage_adapter(tmp_path)
    _run_storage_core_contract(adapter)


def list_wiki_pages_method_D1() -> None:
    """D1 — WikiStoragePort defines list_wiki_pages per ADR-002."""
    assert hasattr(WikiStoragePort, "list_wiki_pages")
    hints = get_type_hints(WikiStoragePort.list_wiki_pages)
    assert hints["return"] == list[str]


def list_wiki_pages_contract_Y3(storage_adapter_impl: WikiStoragePort) -> None:
    """Y3 — binding: fake and filesystem adapter implement list_wiki_pages."""
    adapter = storage_adapter_impl
    adapter.ensure_wiki_layout()
    if isinstance(adapter, InMemoryWikiStorageFake):
        adapter.wiki_pages.update(
            {
                "daily-note.md": "content",
                "topics/page.md": "topic",
            }
        )
    else:
        adapter.write_wiki_page("daily-note.md", "# Daily")
        adapter.write_wiki_page("topics/page.md", "# Topic")
    pages = adapter.list_wiki_pages()
    assert "daily-note.md" in pages
    assert "topics/page.md" in pages
    assert "SCHEMA.md" not in pages
    assert "log.md" not in pages
    assert "index.md" in pages
