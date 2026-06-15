"""Integration tests for LLM provider factory (S11 / S2-6)."""

from __future__ import annotations

from pathlib import Path

import pytest

from contract.fakes import InMemoryConfigurationFake
from llm_wiki.adapters.llm.anthropic import AnthropicLLMAdapter
from llm_wiki.adapters.llm.errors import ProviderUnavailableError
from llm_wiki.adapters.llm.factory import select_llm_provider
from llm_wiki.adapters.llm.ollama import OllamaLLMAdapter
from llm_wiki.adapters.llm.openai import OpenAILLMAdapter


def _base_config(**overrides: object) -> InMemoryConfigurationFake:
    defaults: dict[str, object] = {
        "vault_root": Path("/vault"),
        "wiki_dir": Path("/vault/wiki"),
        "ollama_base_url": "http://127.0.0.1:1",
        "openai_api_key": None,
        "anthropic_api_key": None,
        "provider_override": None,
    }
    defaults.update(overrides)
    return InMemoryConfigurationFake(**defaults)  # type: ignore[arg-type]


def selects_ollama_when_reachable_s11_D1(hermetic_ollama_server: str) -> None:
    """D1 — Ollama reachable + no override → OllamaLLMAdapter."""
    config = _base_config(ollama_base_url=hermetic_ollama_server)
    provider = select_llm_provider(config)
    assert isinstance(provider, OllamaLLMAdapter)


def falls_back_openai_s11_D2(hermetic_ollama_server: str) -> None:
    """D2 — Ollama unreachable + OpenAI key → OpenAI adapter."""
    config = _base_config(
        ollama_base_url="http://127.0.0.1:1",
        openai_api_key="sk-test",
    )
    provider = select_llm_provider(config)
    assert isinstance(provider, OpenAILLMAdapter)


def explicit_anthropic_s11_D3() -> None:
    """D3 — override anthropic + key → Anthropic; missing key raises."""
    config = _base_config(
        provider_override="anthropic",
        anthropic_api_key="sk-ant-test",
    )
    provider = select_llm_provider(config)
    assert isinstance(provider, AnthropicLLMAdapter)

    missing_key = _base_config(provider_override="anthropic", anthropic_api_key=None)
    with pytest.raises(ProviderUnavailableError, match="ANTHROPIC_API_KEY"):
        select_llm_provider(missing_key)


def force_ollama_override_s11_D4(hermetic_ollama_server: str) -> None:
    """D4 — override ollama forces Ollama even when OpenAI key present."""
    config = _base_config(
        ollama_base_url=hermetic_ollama_server,
        provider_override="ollama",
        openai_api_key="sk-test",
    )
    provider = select_llm_provider(config)
    assert isinstance(provider, OllamaLLMAdapter)


def error_when_none_available_s11_D5() -> None:
    """D5 — no provider available → ProviderUnavailableError with guidance."""
    config = _base_config(ollama_base_url="http://127.0.0.1:1")
    with pytest.raises(ProviderUnavailableError) as exc_info:
        select_llm_provider(config)
    message = str(exc_info.value)
    assert "Ollama" in message
    assert "OPENAI_API_KEY" in message or "API" in message


def no_auto_anthropic_s11_D6() -> None:
    """D6 — Anthropic key without override does not auto-select Anthropic."""
    config = _base_config(
        ollama_base_url="http://127.0.0.1:1",
        anthropic_api_key="sk-ant-test",
    )
    with pytest.raises(ProviderUnavailableError):
        select_llm_provider(config)


def selection_order_binding_s11_Y4(
    hermetic_ollama_server: str,
) -> None:
    """Y4 — binding: factory selection order matches ADR-004 (D1–D6)."""
    selects_ollama_when_reachable_s11_D1(hermetic_ollama_server)
    falls_back_openai_s11_D2(hermetic_ollama_server)
    explicit_anthropic_s11_D3()
    force_ollama_override_s11_D4(hermetic_ollama_server)
    error_when_none_available_s11_D5()
    no_auto_anthropic_s11_D6()
