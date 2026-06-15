"""Integration tests for MarkdownSchemaAdapter."""

from __future__ import annotations

from integration.conftest import VaultFixture


def parses_default_excludes_s4_C1(vault_tmp: VaultFixture) -> None:
    """C1 — load() returns ADR-003 default excludes from initialized SCHEMA.md."""
    vault_tmp.storage.ensure_wiki_layout()
    schema = vault_tmp.schema.load()
    assert ".obsidian/" in schema.excludes
    assert "wiki/" in schema.excludes
    assert ".*" in schema.excludes


def parses_custom_exclude_s4_C2(vault_tmp: VaultFixture) -> None:
    """C2 — user-added exclude bullet is included in parsed excludes."""
    vault_tmp.storage.ensure_wiki_layout()
    schema_path = vault_tmp.wiki_dir / "SCHEMA.md"
    content = schema_path.read_text(encoding="utf-8")
    marker = "<!-- User-editable: add more exclude globs below -->"
    updated = content.replace(
        marker,
        f"{marker}\n- `drafts/`\n",
    )
    schema_path.write_text(updated, encoding="utf-8")
    schema = vault_tmp.schema.load()
    assert "drafts/" in schema.excludes


def loads_from_disk_Y4(vault_tmp: VaultFixture) -> None:
    """Y4 — schema adapter reads real SCHEMA.md on disk, not in-memory mock."""
    vault_tmp.storage.ensure_wiki_layout()
    schema_path = vault_tmp.wiki_dir / "SCHEMA.md"
    assert schema_path.is_file()
    before = schema_path.stat().st_mtime_ns
    schema = vault_tmp.schema.load()
    after = schema_path.stat().st_mtime_ns
    assert before == after
    assert len(schema.excludes) >= 3
    assert schema.raw_sections["Excludes"]
