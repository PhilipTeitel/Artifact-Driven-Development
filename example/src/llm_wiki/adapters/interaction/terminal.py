"""Terminal user interaction adapter using Rich (S2-7)."""

from __future__ import annotations

import logging

from rich.console import Console

logger = logging.getLogger(__name__)

_AFFIRMATIVE = frozenset({"y", "yes"})


class TerminalUserInteractionAdapter:
    """UserInteractionPort adapter for terminal stdin/stdout via Rich.

    Batch-mode bypass (``ConfigurationPort.batch_mode``) is the responsibility
    of ingest/query use cases (S2-8, S2-9); adapter methods remain callable.
    """

    def __init__(self, *, console: Console | None = None) -> None:
        self._console = console or Console()

    def present(self, text: str) -> None:
        self._console.print(text)

    def confirm(self, message: str) -> bool:
        """Return True for affirmative input (``y`` or ``yes``, case-insensitive)."""
        self._console.print(f"{message} [y/n]: ", end="")
        response = input().strip().lower()
        return response in _AFFIRMATIVE

    def prompt(self, message: str) -> str:
        self._console.print(f"{message}: ", end="")
        logger.debug("prompt invoked")
        return input().strip()
