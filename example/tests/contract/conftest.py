"""Parametrized adapter fixtures for port contract suites (S2-12)."""

from __future__ import annotations

import os
from collections.abc import Iterator
from io import StringIO
from pathlib import Path

import pytest
from rich.console import Console

from contract.fakes import (
    InMemoryConfigurationFake,
    InMemoryInteractionFake,
    InMemoryLLMFake,
    InMemorySchemaFake,
    InMemoryWikiStorageFake,
)
from llm_wiki.adapters.cli.configuration import CLIFlags, build_cli_configuration
from llm_wiki.adapters.interaction.terminal import TerminalUserInteractionAdapter
from llm_wiki.adapters.llm.ollama import OllamaLLMAdapter
from llm_wiki.adapters.schema.markdown import MarkdownSchemaAdapter
from llm_wiki.adapters.storage.filesystem import FilesystemWikiStorageAdapter
from llm_wiki.ports.configuration import ConfigurationPort
from llm_wiki.ports.interaction import UserInteractionPort
from llm_wiki.ports.llm import LLMPort
from llm_wiki.ports.schema import SchemaPort
from llm_wiki.ports.storage import WikiStoragePort

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = REPO_ROOT / "templates" / "wiki"

STORAGE_ADAPTER_KINDS = ("fake", "filesystem")
SCHEMA_ADAPTER_KINDS = ("fake", "markdown")
CONFIGURATION_ADAPTER_KINDS = ("fake", "cli")
LLM_ADAPTER_KINDS = ("fake", "ollama")
INTERACTION_ADAPTER_KINDS = ("fake", "terminal")

PORT_ADAPTER_FIXTURES = (
    "storage_adapter_impl",
    "schema_adapter_impl",
    "configuration_adapter_impl",
    "llm_adapter_impl",
    "interaction_adapter_impl",
)


def _filesystem_storage_adapter(tmp_path: Path) -> FilesystemWikiStorageAdapter:
    vault_root = tmp_path / "vault"
    vault_root.mkdir()
    (vault_root / "daily").mkdir()
    (vault_root / "daily" / "note.md").write_text("# note\n", encoding="utf-8")
    wiki_dir = vault_root / "wiki"
    config = InMemoryConfigurationFake(vault_root=vault_root, wiki_dir=wiki_dir)
    schema = MarkdownSchemaAdapter(config=config)
    return FilesystemWikiStorageAdapter(
        config=config,
        schema=schema,
        templates_dir=TEMPLATES_DIR,
    )


def _markdown_schema_adapter(tmp_path: Path) -> MarkdownSchemaAdapter:
    vault_root = tmp_path / "vault"
    wiki_dir = vault_root / "wiki"
    wiki_dir.mkdir(parents=True)
    template = TEMPLATES_DIR / "SCHEMA.md"
    (wiki_dir / "SCHEMA.md").write_bytes(template.read_bytes())
    config = InMemoryConfigurationFake(vault_root=vault_root, wiki_dir=wiki_dir)
    return MarkdownSchemaAdapter(config=config)


def _cli_configuration_adapter(tmp_path: Path) -> ConfigurationPort:
    vault = tmp_path / "vault"
    (vault / ".obsidian").mkdir(parents=True)
    keys = (
        "LLM_WIKI_DIR",
        "LLM_WIKI_PROVIDER",
        "OLLAMA_BASE_URL",
        "OLLAMA_MODEL",
        "OPENAI_API_KEY",
        "OPENAI_MODEL",
        "ANTHROPIC_API_KEY",
        "ANTHROPIC_MODEL",
    )
    environ = {k: v for k, v in os.environ.items() if k not in keys}
    return build_cli_configuration(
        flags=CLIFlags(vault=str(vault), provider="ollama", batch=True),
        environ=environ,
    )


@pytest.fixture(params=STORAGE_ADAPTER_KINDS, ids=STORAGE_ADAPTER_KINDS)
def storage_adapter_impl(request: pytest.FixtureRequest, tmp_path: Path) -> WikiStoragePort:
    """WikiStoragePort implemented by fake or filesystem adapter."""
    if request.param == "fake":
        return InMemoryWikiStorageFake(wiki_dir=Path("/vault/wiki"))
    return _filesystem_storage_adapter(tmp_path)


@pytest.fixture(params=SCHEMA_ADAPTER_KINDS, ids=SCHEMA_ADAPTER_KINDS)
def schema_adapter_impl(request: pytest.FixtureRequest, tmp_path: Path) -> SchemaPort:
    """SchemaPort implemented by fake or markdown adapter."""
    if request.param == "fake":
        return InMemorySchemaFake()
    return _markdown_schema_adapter(tmp_path)


@pytest.fixture(params=CONFIGURATION_ADAPTER_KINDS, ids=CONFIGURATION_ADAPTER_KINDS)
def configuration_adapter_impl(
    request: pytest.FixtureRequest,
    tmp_path: Path,
) -> ConfigurationPort:
    """ConfigurationPort implemented by fake or CLI adapter."""
    if request.param == "fake":
        return InMemoryConfigurationFake(
            vault_root=Path("/vault"),
            wiki_dir=Path("/vault/wiki"),
            batch_mode=True,
            provider_override="ollama",
        )
    return _cli_configuration_adapter(tmp_path)


@pytest.fixture(params=LLM_ADAPTER_KINDS, ids=LLM_ADAPTER_KINDS)
def llm_adapter_impl(
    request: pytest.FixtureRequest,
    hermetic_ollama_server: str,
) -> LLMPort:
    """LLMPort implemented by fake or Ollama adapter against hermetic server."""
    if request.param == "fake":
        return InMemoryLLMFake()
    config = InMemoryConfigurationFake(
        vault_root=Path("/vault"),
        wiki_dir=Path("/vault/wiki"),
        ollama_base_url=hermetic_ollama_server,
    )
    return OllamaLLMAdapter(config)


@pytest.fixture(params=INTERACTION_ADAPTER_KINDS, ids=INTERACTION_ADAPTER_KINDS)
def interaction_adapter_impl(
    request: pytest.FixtureRequest,
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[UserInteractionPort]:
    """UserInteractionPort implemented by fake or terminal adapter."""
    if request.param == "fake":
        yield InMemoryInteractionFake(
            confirm_responses={"Proceed?": True},
            prompt_responses={"Name:": "alice"},
        )
        return
    buffer = StringIO()
    console = Console(file=buffer, force_terminal=True, width=80)
    adapter = TerminalUserInteractionAdapter(console=console)
    responses = iter(["y", "alice"])
    monkeypatch.setattr("builtins.input", lambda: next(responses))
    yield adapter


def parametrize_adapters_A1() -> None:
    """A1 — contract conftest exposes parametrized fake and real adapter fixtures."""
    kind_sets = (
        STORAGE_ADAPTER_KINDS,
        SCHEMA_ADAPTER_KINDS,
        CONFIGURATION_ADAPTER_KINDS,
        LLM_ADAPTER_KINDS,
        INTERACTION_ADAPTER_KINDS,
    )
    assert len(kind_sets) == len(PORT_ADAPTER_FIXTURES)
    for kinds in kind_sets:
        assert len(kinds) >= 2
        assert "fake" in kinds
    for fixture_name in PORT_ADAPTER_FIXTURES:
        assert fixture_name in globals(), f"missing fixture {fixture_name}"
