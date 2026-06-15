"""Integration tests for FilesystemWikiStorageAdapter."""

from __future__ import annotations

import json

import pytest

from integration.conftest import TEMPLATES_DIR, VaultFixture
from llm_wiki.adapters.storage.filesystem import WikiStorageBoundaryError


def creates_wiki_layout_s1_A1(vault_tmp: VaultFixture) -> None:
    """A1 — ensure_wiki_layout creates SCHEMA.md, index.md, log.md."""
    result = vault_tmp.storage.ensure_wiki_layout()
    assert set(result.created) == {"SCHEMA.md", "index.md", "log.md"}
    for name in ("SCHEMA.md", "index.md", "log.md"):
        assert (vault_tmp.wiki_dir / name).is_file()


def templates_match_repo_s1_A2(vault_tmp: VaultFixture) -> None:
    """A2 — created files match repo templates byte-for-byte."""
    vault_tmp.storage.ensure_wiki_layout()
    for name in ("SCHEMA.md", "index.md", "log.md"):
        created = (vault_tmp.wiki_dir / name).read_bytes()
        template = (TEMPLATES_DIR / name).read_bytes()
        assert created == template


def sources_unmodified_s5_A3(vault_tmp: VaultFixture) -> None:
    """A3 — vault sources unchanged after init."""
    source = vault_tmp.vault_root / "daily" / "sample.md"
    before_bytes = source.read_bytes()
    before_mtime = source.stat().st_mtime_ns
    vault_tmp.storage.ensure_wiki_layout()
    assert source.read_bytes() == before_bytes
    assert source.stat().st_mtime_ns == before_mtime


def idempotent_init_s2_B1(vault_tmp: VaultFixture) -> None:
    """B1 — second ensure_wiki_layout reports already_present only."""
    first = vault_tmp.storage.ensure_wiki_layout()
    assert set(first.created) == {"SCHEMA.md", "index.md", "log.md"}
    second = vault_tmp.storage.ensure_wiki_layout()
    assert second.created == ()
    assert set(second.already_present) == {"SCHEMA.md", "index.md", "log.md"}


def preserves_wiki_pages_s2_B2(vault_tmp: VaultFixture) -> None:
    """B2 — existing custom wiki page content preserved on re-init."""
    vault_tmp.wiki_dir.mkdir(parents=True, exist_ok=True)
    page = vault_tmp.wiki_dir / "existing-page.md"
    custom = "# Custom page\n\nDo not overwrite.\n"
    page.write_text(custom, encoding="utf-8")
    vault_tmp.storage.ensure_wiki_layout()
    vault_tmp.storage.ensure_wiki_layout()
    assert page.read_text(encoding="utf-8") == custom


def creates_missing_only_s2_B3(vault_tmp: VaultFixture) -> None:
    """B3 — partial layout creates only missing init artifacts."""
    vault_tmp.wiki_dir.mkdir(parents=True, exist_ok=True)
    schema_only = TEMPLATES_DIR / "SCHEMA.md"
    (vault_tmp.wiki_dir / "SCHEMA.md").write_bytes(schema_only.read_bytes())
    result = vault_tmp.storage.ensure_wiki_layout()
    assert result.created == ("index.md", "log.md")
    assert result.already_present == ("SCHEMA.md",)


def list_sources_respects_excludes_s7_D1(vault_tmp: VaultFixture) -> None:
    """D1 — list_sources excludes wiki and .obsidian paths."""
    vault_tmp.storage.ensure_wiki_layout()
    sources = vault_tmp.storage.list_sources()
    assert "daily/sample.md" in sources
    assert not any(path.startswith(".obsidian/") for path in sources)
    assert not any(path.startswith("wiki/") for path in sources)


def rejects_outside_wiki_write_s5_D2(vault_tmp: VaultFixture) -> None:
    """D2 — write methods reject paths outside wiki dir."""
    vault_tmp.storage.ensure_wiki_layout()
    source = vault_tmp.vault_root / "daily" / "sample.md"
    before = source.read_bytes()
    with pytest.raises(WikiStorageBoundaryError):
        vault_tmp.storage.write_wiki_page("../daily/sample.md", "tampered")
    assert source.read_bytes() == before


def ingested_sidecar_round_trip_s12_E1(vault_tmp: VaultFixture) -> None:
    """E1 — write_ingested/read_ingested round-trip with normalized keys."""
    vault_tmp.storage.ensure_wiki_layout()
    payload = {
        "version": 1,
        "sources": {
            "daily\\sample.md": "2026-06-01T12:00:00Z",
            "notes/article.md": "2026-06-01T13:00:00Z",
        },
    }
    vault_tmp.storage.write_ingested(payload)
    loaded = vault_tmp.storage.read_ingested()
    assert loaded["version"] == 1
    assert loaded["sources"]["daily/sample.md"] == "2026-06-01T12:00:00Z"
    assert loaded["sources"]["notes/article.md"] == "2026-06-01T13:00:00Z"


def sidecar_does_not_touch_source_s12_E2(vault_tmp: VaultFixture) -> None:
    """E2 — sidecar write does not modify referenced source file."""
    vault_tmp.storage.ensure_wiki_layout()
    source = vault_tmp.vault_root / "daily" / "sample.md"
    before = source.read_bytes()
    vault_tmp.storage.write_ingested(
        {"version": 1, "sources": {"daily/sample.md": "2026-06-01T12:00:00Z"}}
    )
    assert source.read_bytes() == before


def append_only_log_s13_F1(vault_tmp: VaultFixture) -> None:
    """F1 — append_log preserves prior log.md bytes."""
    vault_tmp.storage.ensure_wiki_layout()
    log_path = vault_tmp.wiki_dir / "log.md"
    prior = log_path.read_bytes()
    entry = "\n## [2026-06-01] init | test entry\nBody text.\n"
    vault_tmp.storage.append_log(entry)
    updated = log_path.read_bytes()
    assert updated.startswith(prior)
    assert updated.endswith(entry.encode("utf-8"))


def real_disk_layout_Y1(vault_tmp: VaultFixture) -> None:
    """Y1 — real disk writes under wiki dir via pathlib only."""
    vault_tmp.storage.ensure_wiki_layout()
    assert vault_tmp.wiki_dir.is_dir()
    assert (vault_tmp.wiki_dir / "SCHEMA.md").is_file()


def sources_immutable_binding_s5_Y2(vault_tmp: VaultFixture) -> None:
    """Y2 — source file unchanged after init and sidecar write."""
    source = vault_tmp.vault_root / "daily" / "sample.md"
    before = source.read_bytes()
    vault_tmp.storage.ensure_wiki_layout()
    vault_tmp.storage.write_ingested(
        {"version": 1, "sources": {"daily/sample.md": "2026-06-01T12:00:00Z"}}
    )
    assert source.read_bytes() == before


def list_wiki_pages_D2(vault_tmp: VaultFixture) -> None:
    """D2 — list_wiki_pages returns seeded pages excluding schema/log artifacts."""
    vault_tmp.storage.ensure_wiki_layout()
    vault_tmp.storage.write_wiki_page("daily-note.md", "# Daily\n")
    vault_tmp.storage.write_wiki_page("topics/overview.md", "# Topics\n")
    pages = vault_tmp.storage.list_wiki_pages()
    assert "daily-note.md" in pages
    assert "topics/overview.md" in pages
    assert "SCHEMA.md" not in pages
    assert "log.md" not in pages


def list_wiki_pages_binding_Y2(vault_tmp: VaultFixture) -> None:
    """Y2 — binding: real filesystem adapter lists pages from temp vault."""
    vault_tmp.storage.ensure_wiki_layout()
    vault_tmp.storage.write_wiki_page("seeded-page.md", "# Seeded\n")
    assert "seeded-page.md" in vault_tmp.storage.list_wiki_pages()


def ingested_adr003_shape_Y3(vault_tmp: VaultFixture) -> None:
    """Y3 — .ingested.json on disk matches ADR-003 schema."""
    vault_tmp.storage.ensure_wiki_layout()
    vault_tmp.storage.write_ingested(
        {"version": 1, "sources": {"daily/sample.md": "2026-06-01T12:00:00Z"}}
    )
    sidecar_path = vault_tmp.wiki_dir / ".ingested.json"
    on_disk = json.loads(sidecar_path.read_text(encoding="utf-8"))
    assert on_disk == {
        "version": 1,
        "sources": {"daily/sample.md": "2026-06-01T12:00:00Z"},
    }
