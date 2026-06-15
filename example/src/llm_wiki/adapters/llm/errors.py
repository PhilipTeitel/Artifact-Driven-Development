"""LLM adapter errors (S2-6)."""

from __future__ import annotations


class ProviderUnavailableError(RuntimeError):
    """Raised when no LLM provider can be selected (ADR-004 / S11)."""

    def __init__(self, message: str | None = None) -> None:
        super().__init__(
            message
            or (
                "No LLM provider available. Start Ollama (e.g. `ollama serve`) or set "
                "OPENAI_API_KEY / ANTHROPIC_API_KEY (use --provider anthropic for Anthropic)."
            )
        )
