"""Shared fixtures for integration tests."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

import pytest

from contract.fakes import InMemoryConfigurationFake
from llm_wiki.adapters.schema.markdown import MarkdownSchemaAdapter
from llm_wiki.adapters.storage.filesystem import FilesystemWikiStorageAdapter
from llm_wiki.ports.configuration import ConfigurationPort

REPO_ROOT = Path(__file__).resolve().parents[2]
VAULT_SEED = REPO_ROOT / "tests" / "fixtures" / "vault"
TEMPLATES_DIR = REPO_ROOT / "templates" / "wiki"


@dataclass(frozen=True)
class VaultFixture:
    """Hermetic vault copy with adapters wired to temp paths."""

    vault_root: Path
    wiki_dir: Path
    config: ConfigurationPort
    storage: FilesystemWikiStorageAdapter
    schema: MarkdownSchemaAdapter


@pytest.fixture
def vault_tmp(tmp_path: Path) -> VaultFixture:
    """Copy seed vault into tmp_path and return wired adapters."""
    vault_root = tmp_path / "vault"
    shutil.copytree(VAULT_SEED, vault_root)
    wiki_dir = vault_root / "wiki"
    config = InMemoryConfigurationFake(vault_root=vault_root, wiki_dir=wiki_dir)
    schema = MarkdownSchemaAdapter(config=config)
    storage = FilesystemWikiStorageAdapter(
        config=config,
        schema=schema,
        templates_dir=TEMPLATES_DIR,
    )
    return VaultFixture(
        vault_root=vault_root,
        wiki_dir=wiki_dir,
        config=config,
        storage=storage,
        schema=schema,
    )
