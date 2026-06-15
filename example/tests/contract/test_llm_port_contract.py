"""Contract tests for LLMPort."""

from __future__ import annotations

from pathlib import Path
from typing import get_type_hints

from llm_wiki.adapters.llm.ollama import OllamaLLMAdapter
from llm_wiki.ports.llm import LLMPort

from .conftest import InMemoryConfigurationFake
from .fakes import InMemoryLLMFake


def _run_llm_core_contract(adapter: LLMPort) -> None:
    """Shared behavioral suite for fake and Ollama adapters."""
    assert isinstance(adapter, LLMPort)
    assert adapter.is_available() is True
    reply = adapter.complete("ping")
    assert isinstance(reply, str)
    assert reply


def llm_methods_A2() -> None:
    """LLMPort defines complete and is_available."""
    assert "complete" in LLMPort.__dict__ or hasattr(LLMPort, "complete")
    hints = get_type_hints(LLMPort.complete)
    assert hints["prompt"] is str
    assert hints["return"] is str
    assert hasattr(LLMPort, "is_available")


def llm_core_contract_A1(llm_adapter_impl: LLMPort) -> None:
    """A1 — core LLM contract runs against parametrized fake and Ollama adapters."""
    _run_llm_core_contract(llm_adapter_impl)


def llm_fake_round_trip_C2() -> None:
    """Fake complete returns deterministic text; is_available toggles."""
    fake = InMemoryLLMFake(available=True)
    assert fake.complete("hello") == "echo:hello"
    assert fake.complete("hello", system="sys") == "[system:sys] echo:hello"
    assert fake.is_available() is True
    fake.available = False
    assert fake.is_available() is False


def llm_contract_Y5() -> None:
    """Reference fake satisfies LLMPort contract."""
    fake = InMemoryLLMFake()
    assert isinstance(fake, LLMPort)
    assert fake.complete("ping") == "echo:ping"


def ollama_passes_contract_E1(hermetic_ollama_server: str) -> None:
    """E1 — Ollama adapter satisfies LLMPort contract against hermetic server."""
    config = InMemoryConfigurationFake(
        vault_root=Path("/vault"),
        wiki_dir=Path("/vault/wiki"),
        ollama_base_url=hermetic_ollama_server,
    )
    adapter = OllamaLLMAdapter(config)
    _run_llm_core_contract(adapter)
    assert adapter.complete("ping") == "assistant reply from hermetic server"
    assert adapter.complete("ping", system="sys") == "assistant reply from hermetic server"
