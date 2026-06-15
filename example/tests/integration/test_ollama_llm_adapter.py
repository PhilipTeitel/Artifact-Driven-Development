"""Integration tests for OllamaLLMAdapter (S2-6)."""

from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from contract.fakes import InMemoryConfigurationFake
from integration.llm.conftest import _HermeticOllamaHandler
from llm_wiki.adapters.llm import ollama as ollama_module
from llm_wiki.adapters.llm.ollama import OllamaLLMAdapter


def _config_for(base_url: str, *, model: str = "llama3.2") -> InMemoryConfigurationFake:
    return InMemoryConfigurationFake(
        vault_root=Path("/vault"),
        wiki_dir=Path("/vault/wiki"),
        ollama_base_url=base_url,
        ollama_model=model,
    )


def ollama_available_hermetic_A1(hermetic_ollama_server: str) -> None:
    """A1 — is_available() is True when hermetic server responds on /api/tags."""
    adapter = OllamaLLMAdapter(_config_for(hermetic_ollama_server))
    assert adapter.is_available() is True


def ollama_complete_round_trip_A2(hermetic_ollama_server: str) -> None:
    """A2 — complete() returns assistant text from hermetic /api/chat JSON."""
    adapter = OllamaLLMAdapter(_config_for(hermetic_ollama_server))
    result = adapter.complete("hello")
    assert result == "assistant reply from hermetic server"


def ollama_respects_config_A3(hermetic_ollama_server: str) -> None:
    """A3 — uses config.ollama_base_url and config.ollama_model."""
    config = _config_for(hermetic_ollama_server, model="custom-model")
    adapter = OllamaLLMAdapter(config)
    adapter.complete("ping")
    assert _HermeticOllamaHandler.last_chat_payload is not None
    assert _HermeticOllamaHandler.last_chat_payload["model"] == "custom-model"


def httpx_binding_Y1(hermetic_ollama_server: str) -> None:
    """Y1 — binding: adapter uses httpx against hermetic HTTP server."""
    assert ollama_module.httpx is httpx
    adapter = OllamaLLMAdapter(_config_for(hermetic_ollama_server))
    assert isinstance(adapter._client, httpx.Client)  # noqa: SLF001
    assert adapter.complete("binding") == "assistant reply from hermetic server"


def ollama_resolves_tag_prefix_F2(hermetic_ollama_server: str) -> None:
    """F2 — resolve llama3.2 to an installed llama3.2:<tag> model name."""
    _HermeticOllamaHandler.installed_models = ["llama3.2:latest"]
    adapter = OllamaLLMAdapter(_config_for(hermetic_ollama_server, model="llama3.2"))
    adapter.complete("ping")
    assert _HermeticOllamaHandler.last_chat_payload is not None
    assert _HermeticOllamaHandler.last_chat_payload["model"] == "llama3.2:latest"


def ollama_fallback_default_model_F2(hermetic_ollama_server: str) -> None:
    """F2 — when default model is missing, use the first installed model."""
    _HermeticOllamaHandler.installed_models = ["mistral:latest"]
    adapter = OllamaLLMAdapter(_config_for(hermetic_ollama_server))
    adapter.complete("ping")
    assert _HermeticOllamaHandler.last_chat_payload is not None
    assert _HermeticOllamaHandler.last_chat_payload["model"] == "mistral:latest"


def ollama_raises_on_model_not_found_F2(hermetic_ollama_server: str) -> None:
    """F2 — chat 404 raises ValueError listing installed models and pull guidance."""
    _HermeticOllamaHandler.chat_status = 404
    _HermeticOllamaHandler.chat_error = "model 'llama3.2' not found"
    adapter = OllamaLLMAdapter(_config_for(hermetic_ollama_server))
    with pytest.raises(ValueError) as exc_info:
        adapter.complete("ping")
    message = str(exc_info.value)
    assert "Ollama model 'llama3.2' not found" in message
    assert "Installed models: llama3.2" in message
    assert "ollama pull llama3.2" in message
