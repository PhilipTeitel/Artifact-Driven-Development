"""Integration tests for TerminalUserInteractionAdapter (S2-7)."""

from __future__ import annotations

from io import StringIO

import pytest
from rich.console import Console

from llm_wiki.adapters.interaction.terminal import TerminalUserInteractionAdapter


def _adapter_with_output() -> tuple[TerminalUserInteractionAdapter, StringIO]:
    buffer = StringIO()
    console = Console(file=buffer, force_terminal=True, width=80)
    return TerminalUserInteractionAdapter(console=console), buffer


def present_writes_output_A1() -> None:
    """A1 — present() writes text to configured console output."""
    adapter, buffer = _adapter_with_output()
    adapter.present("hello")
    assert "hello" in buffer.getvalue()


def confirm_yes_s8_B1(monkeypatch: pytest.MonkeyPatch) -> None:
    """B1 — confirm() returns True on affirmative stdin."""
    adapter, _buffer = _adapter_with_output()
    monkeypatch.setattr("builtins.input", lambda: "yes")
    assert adapter.confirm("Proceed?") is True


def confirm_yes_case_insensitive_B1(monkeypatch: pytest.MonkeyPatch) -> None:
    """B1 — confirm() accepts uppercase Y."""
    adapter, _buffer = _adapter_with_output()
    monkeypatch.setattr("builtins.input", lambda: "Y")
    assert adapter.confirm("Proceed?") is True


def confirm_no_s8_B2(monkeypatch: pytest.MonkeyPatch) -> None:
    """B2 — confirm() returns False on negative input without raising."""
    adapter, _buffer = _adapter_with_output()
    monkeypatch.setattr("builtins.input", lambda: "n")
    assert adapter.confirm("Proceed?") is False


def prompt_returns_input_C1(monkeypatch: pytest.MonkeyPatch) -> None:
    """C1 — prompt() returns stripped user input from stdin."""
    adapter, _buffer = _adapter_with_output()
    monkeypatch.setattr("builtins.input", lambda: "  alice  ")
    assert adapter.prompt("Name") == "alice"


def rich_console_binding_Y1() -> None:
    """Y1 — binding: adapter uses injectable Rich Console for output."""
    adapter, buffer = _adapter_with_output()
    assert isinstance(adapter._console, Console)  # noqa: SLF001
    adapter.present("rich")
    assert "rich" in buffer.getvalue()
