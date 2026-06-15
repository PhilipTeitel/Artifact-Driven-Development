"""Composition-root adapter assembly for the Typer CLI (S2-11)."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from llm_wiki.adapters.cli.configuration import (
    CLIFlags,
    build_cli_configuration,
)
from llm_wiki.adapters.interaction.terminal import TerminalUserInteractionAdapter
from llm_wiki.adapters.llm.factory import select_llm_provider
from llm_wiki.adapters.schema.markdown import MarkdownSchemaAdapter
from llm_wiki.adapters.storage.filesystem import FilesystemWikiStorageAdapter
from llm_wiki.ports.configuration import ConfigurationPort
from llm_wiki.ports.interaction import UserInteractionPort
from llm_wiki.ports.llm import LLMPort
from llm_wiki.ports.schema import SchemaPort
from llm_wiki.ports.storage import WikiStoragePort


@dataclass(frozen=True)
class WiringOverrides:
    """Test hooks for substituting driven adapters at the composition root."""

    llm: LLMPort | None = None
    interaction: UserInteractionPort | None = None


@dataclass(frozen=True)
class AppContext:
    """Wired driven adapters and configuration for use case construction."""

    config: ConfigurationPort
    storage: WikiStoragePort
    schema: SchemaPort
    interaction: UserInteractionPort
    llm: LLMPort | None = None


def build_context(
    *,
    flags: CLIFlags | None = None,
    start_path: Path | None = None,
    environ: Mapping[str, str] | None = None,
    overrides: WiringOverrides | None = None,
    require_llm: bool = False,
) -> AppContext:
    """Assemble driven adapters from CLI flags and environment."""
    config = build_cli_configuration(
        flags=flags,
        start_path=start_path,
        environ=environ if environ is not None else os.environ,
    )
    schema = MarkdownSchemaAdapter(config=config)
    storage = FilesystemWikiStorageAdapter(config=config, schema=schema)
    if overrides and overrides.interaction is not None:
        interaction = overrides.interaction
    else:
        interaction = TerminalUserInteractionAdapter()
    llm: LLMPort | None = None
    if overrides and overrides.llm is not None:
        llm = overrides.llm
    elif require_llm:
        llm = select_llm_provider(config)
    return AppContext(
        config=config,
        storage=storage,
        schema=schema,
        interaction=interaction,
        llm=llm,
    )