"""CLI configuration adapter implementing ConfigurationPort (ADR-004)."""

from __future__ import annotations

import logging
import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from llm_wiki.adapters.cli.errors import ConfigurationError
from llm_wiki.adapters.cli.vault_walk import validate_vault_path, walk_up_to_vault
from llm_wiki.ports.configuration import ConfigurationPort

logger = logging.getLogger(__name__)

DEFAULT_WIKI_SUBDIR = "wiki"
DEFAULT_OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_OLLAMA_MODEL = "llama3.2"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"

_ENV_WIKI_DIR = "LLM_WIKI_DIR"
_ENV_PROVIDER = "LLM_WIKI_PROVIDER"
_ENV_OLLAMA_BASE_URL = "OLLAMA_BASE_URL"
_ENV_OLLAMA_MODEL = "OLLAMA_MODEL"
_ENV_OPENAI_API_KEY = "OPENAI_API_KEY"
_ENV_OPENAI_MODEL = "OPENAI_MODEL"
_ENV_ANTHROPIC_API_KEY = "ANTHROPIC_API_KEY"
_ENV_ANTHROPIC_MODEL = "ANTHROPIC_MODEL"

_VALID_PROVIDERS = frozenset({"ollama", "openai", "anthropic"})


@dataclass(frozen=True)
class CLIFlags:
    """Explicit CLI flag values for testability without Typer context."""

    vault: str | None = None
    wiki_dir: str | None = None
    provider: str | None = None
    batch: bool = False


@dataclass(frozen=True)
class CLIConfigurationAdapter:
    """Immutable ConfigurationPort backed by env vars and CLI flags."""

    vault_root: Path
    wiki_dir: Path
    batch_mode: bool
    provider_override: str | None
    ollama_base_url: str
    ollama_model: str
    openai_api_key: str | None
    openai_model: str
    anthropic_api_key: str | None
    anthropic_model: str


def _env_value(environ: Mapping[str, str], key: str) -> str | None:
    value = environ.get(key)
    if value is None or value == "":
        return None
    return value


def _resolve_wiki_subdir(flags: CLIFlags, environ: Mapping[str, str]) -> str:
    if flags.wiki_dir is not None:
        return flags.wiki_dir
    return _env_value(environ, _ENV_WIKI_DIR) or DEFAULT_WIKI_SUBDIR


def _resolve_provider(flags: CLIFlags, environ: Mapping[str, str]) -> str | None:
    if flags.provider is not None:
        provider = flags.provider.lower()
        if provider not in _VALID_PROVIDERS:
            raise ConfigurationError(
                f"Invalid provider {flags.provider!r}; expected one of: "
                + ", ".join(sorted(_VALID_PROVIDERS))
            )
        return provider
    env_provider = _env_value(environ, _ENV_PROVIDER)
    if env_provider is None:
        return None
    provider = env_provider.lower()
    if provider not in _VALID_PROVIDERS:
        raise ConfigurationError(
            f"Invalid {_ENV_PROVIDER}={env_provider!r}; expected one of: "
            + ", ".join(sorted(_VALID_PROVIDERS))
        )
    return provider


def _resolve_vault_root(
    flags: CLIFlags,
    *,
    wiki_subdir: str,
    start_path: Path | None,
) -> Path:
    if flags.vault is not None:
        return validate_vault_path(Path(flags.vault), wiki_subdir=wiki_subdir)
    return walk_up_to_vault(start_path, wiki_subdir=wiki_subdir)


def build_cli_configuration(
    *,
    flags: CLIFlags | None = None,
    environ: Mapping[str, str] | None = None,
    start_path: Path | None = None,
) -> CLIConfigurationAdapter:
    """Build immutable configuration from CLI flags and environment."""
    resolved_flags = flags or CLIFlags()
    resolved_environ = environ if environ is not None else os.environ

    wiki_subdir = _resolve_wiki_subdir(resolved_flags, resolved_environ)
    vault_root = _resolve_vault_root(
        resolved_flags,
        wiki_subdir=wiki_subdir,
        start_path=start_path,
    )
    wiki_dir = (vault_root / wiki_subdir).resolve()
    provider_override = _resolve_provider(resolved_flags, resolved_environ)

    config = CLIConfigurationAdapter(
        vault_root=vault_root,
        wiki_dir=wiki_dir,
        batch_mode=resolved_flags.batch,
        provider_override=provider_override,
        ollama_base_url=_env_value(resolved_environ, _ENV_OLLAMA_BASE_URL)
        or DEFAULT_OLLAMA_BASE_URL,
        ollama_model=_env_value(resolved_environ, _ENV_OLLAMA_MODEL) or DEFAULT_OLLAMA_MODEL,
        openai_api_key=_env_value(resolved_environ, _ENV_OPENAI_API_KEY),
        openai_model=_env_value(resolved_environ, _ENV_OPENAI_MODEL) or DEFAULT_OPENAI_MODEL,
        anthropic_api_key=_env_value(resolved_environ, _ENV_ANTHROPIC_API_KEY),
        anthropic_model=_env_value(resolved_environ, _ENV_ANTHROPIC_MODEL)
        or DEFAULT_ANTHROPIC_MODEL,
    )

    logger.debug(
        "Resolved vault_root=%s provider_override=%r",
        config.vault_root,
        provider_override,
    )
    return config


def assert_configuration_port(config: CLIConfigurationAdapter) -> ConfigurationPort:
    """Narrow type for callers expecting ConfigurationPort."""
    return config
