"""Configuration port — resolved runtime settings (ADR-002)."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable


@runtime_checkable
class ConfigurationPort(Protocol):
    """Resolved runtime settings. Adapters implement; use cases read only."""

    @property
    def vault_root(self) -> Path:
        """Absolute vault directory."""

    @property
    def wiki_dir(self) -> Path:
        """Absolute path to wiki subdirectory."""

    @property
    def batch_mode(self) -> bool:
        """True when --batch (ingest)."""

    @property
    def provider_override(self) -> str | None:
        """Explicit provider: ollama, openai, anthropic."""

    @property
    def ollama_base_url(self) -> str:
        """Ollama HTTP base URL."""

    @property
    def ollama_model(self) -> str:
        """Ollama model name."""

    @property
    def openai_api_key(self) -> str | None:
        """OpenAI API key."""

    @property
    def openai_model(self) -> str:
        """OpenAI model name."""

    @property
    def anthropic_api_key(self) -> str | None:
        """Anthropic API key."""

    @property
    def anthropic_model(self) -> str:
        """Anthropic model name."""
