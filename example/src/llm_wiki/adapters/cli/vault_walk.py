"""Vault root detection via parent-directory walk-up (ADR-003)."""

from __future__ import annotations

from pathlib import Path

from llm_wiki.adapters.cli.errors import VaultNotFoundError

_VAULT_NOT_FOUND_MESSAGE = (
    "Could not find an Obsidian vault. Open your vault folder in the workspace, "
    "or pass --vault PATH to point at the vault root "
    "(a directory containing .obsidian/ or {wiki_subdir}/SCHEMA.md)."
)


def is_vault_root(path: Path, wiki_subdir: str = "wiki") -> bool:
    """Return True when path looks like a vault root per ADR-003."""
    if (path / ".obsidian").is_dir():
        return True
    return (path / wiki_subdir / "SCHEMA.md").is_file()


def walk_up_to_vault(
    start: Path | None = None,
    *,
    wiki_subdir: str = "wiki",
) -> Path:
    """Walk from start (default CWD) toward filesystem root; return first vault root."""
    current = (start or Path.cwd()).resolve()
    root = current.anchor
    while True:
        if is_vault_root(current, wiki_subdir):
            return current
        if current == root or current.parent == current:
            break
        current = current.parent
    raise VaultNotFoundError(_VAULT_NOT_FOUND_MESSAGE.format(wiki_subdir=wiki_subdir))


def validate_vault_path(path: Path, *, wiki_subdir: str = "wiki") -> Path:
    """Validate an explicit vault path without creating wiki artifacts."""
    resolved = path.expanduser().resolve()
    if not resolved.is_dir():
        raise VaultNotFoundError(
            f"Vault path is not a directory: {resolved}\n"
            + _VAULT_NOT_FOUND_MESSAGE.format(wiki_subdir=wiki_subdir)
        )
    if not is_vault_root(resolved, wiki_subdir):
        raise VaultNotFoundError(
            f"Path is not a valid vault root: {resolved}\n"
            + _VAULT_NOT_FOUND_MESSAGE.format(wiki_subdir=wiki_subdir)
        )
    return resolved
