"""User interaction port (ADR-002)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class UserInteractionPort(Protocol):
    """Terminal or future UI prompts."""

    def confirm(self, message: str) -> bool:
        """Query filing, interactive ingest checkpoints."""

    def present(self, text: str) -> None:
        """Show takeaways or reports to user."""

    def prompt(self, message: str) -> str:
        """Optional text input."""
