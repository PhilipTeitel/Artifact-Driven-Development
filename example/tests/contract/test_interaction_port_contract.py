"""Contract tests for UserInteractionPort."""

from __future__ import annotations

import pytest

from llm_wiki.ports.interaction import UserInteractionPort

from .fakes import InMemoryInteractionFake


def _run_interaction_core_contract(adapter: UserInteractionPort) -> None:
    """Shared behavioral suite for fake and terminal adapters."""
    assert isinstance(adapter, UserInteractionPort)
    assert adapter.confirm("Proceed?") is True
    adapter.present("report")
    assert adapter.prompt("Name:") == "alice"


def interaction_methods_A5() -> None:
    """UserInteractionPort defines confirm, present, prompt."""
    for name in ("confirm", "present", "prompt"):
        assert hasattr(UserInteractionPort, name)


def interaction_core_contract_A1(interaction_adapter_impl: UserInteractionPort) -> None:
    """A1 — core interaction contract runs against parametrized fake and terminal adapters."""
    if isinstance(interaction_adapter_impl, InMemoryInteractionFake):
        interaction_adapter_impl.confirm_responses = {"Proceed?": True}
        interaction_adapter_impl.prompt_responses = {"Name:": "alice"}
    _run_interaction_core_contract(interaction_adapter_impl)


def interaction_contract_Y5() -> None:
    """Reference fake satisfies UserInteractionPort contract."""
    fake = InMemoryInteractionFake(
        confirm_responses={"Proceed?": True},
        prompt_responses={"Name:": "alice"},
    )
    assert isinstance(fake, UserInteractionPort)
    assert fake.confirm("Proceed?") is True
    fake.present("report")
    assert fake.presented == ["report"]
    assert fake.prompt("Name:") == "alice"


def _run_terminal_contract(monkeypatch: pytest.MonkeyPatch) -> None:
    from io import StringIO

    from rich.console import Console

    from llm_wiki.adapters.interaction.terminal import TerminalUserInteractionAdapter

    buffer = StringIO()
    console = Console(file=buffer, force_terminal=True, width=80)
    adapter = TerminalUserInteractionAdapter(console=console)
    responses = iter(["y", "alice"])
    monkeypatch.setattr("builtins.input", lambda: next(responses))
    _run_interaction_core_contract(adapter)
    assert "report" in buffer.getvalue()


def terminal_passes_contract_D1(monkeypatch: pytest.MonkeyPatch) -> None:
    """D1 — terminal adapter satisfies UserInteractionPort contract."""
    _run_terminal_contract(monkeypatch)


def terminal_passes_contract_Y2(monkeypatch: pytest.MonkeyPatch) -> None:
    """Y2 — binding: interaction contract suite passes against terminal adapter."""
    _run_terminal_contract(monkeypatch)
