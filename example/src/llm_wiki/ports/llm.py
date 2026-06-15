"""LLM completion port (ADR-002)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class LLMPort(Protocol):
    """Single interface for all LLM operations (ingest, query, lint)."""

    def complete(self, prompt: str, *, system: str | None = None) -> str:
        """Synchronous completion for v1."""

    def is_available(self) -> bool:
        """Health check for provider selection."""
