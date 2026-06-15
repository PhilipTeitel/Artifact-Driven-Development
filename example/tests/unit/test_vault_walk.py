"""Unit tests for vault walk-up helper."""

from __future__ import annotations

from pathlib import Path

import pytest

from llm_wiki.adapters.cli.errors import VaultNotFoundError
from llm_wiki.adapters.cli.vault_walk import is_vault_root, walk_up_to_vault


def _make_obsidian_vault(root: Path) -> Path:
    (root / ".obsidian").mkdir(parents=True)
    return root


def stops_at_filesystem_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Walk-up stops at filesystem root without infinite loop."""
    orphan = tmp_path / "orphan" / "deep"
    orphan.mkdir(parents=True)
    monkeypatch.chdir(orphan)
    with pytest.raises(VaultNotFoundError):
        walk_up_to_vault(orphan)


def finds_obsidian_in_parent(tmp_path: Path) -> None:
    vault = _make_obsidian_vault(tmp_path / "vault")
    nested = vault / "notes" / "daily"
    nested.mkdir(parents=True)
    assert walk_up_to_vault(nested) == vault.resolve()


def finds_schema_marker_without_obsidian(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    wiki = vault / "custom-wiki"
    wiki.mkdir(parents=True)
    (wiki / "SCHEMA.md").write_text("# schema\n", encoding="utf-8")
    nested = vault / "src" / "deep"
    nested.mkdir(parents=True)
    assert walk_up_to_vault(nested, wiki_subdir="custom-wiki") == vault.resolve()
    assert is_vault_root(vault, "custom-wiki")
