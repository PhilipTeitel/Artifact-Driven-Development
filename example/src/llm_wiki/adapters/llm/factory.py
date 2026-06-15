"""LLM provider factory implementing ADR-004 selection (S11 / S2-6)."""

from __future__ import annotations

from llm_wiki.adapters.llm.anthropic import AnthropicLLMAdapter
from llm_wiki.adapters.llm.errors import ProviderUnavailableError
from llm_wiki.adapters.llm.ollama import OllamaLLMAdapter
from llm_wiki.adapters.llm.openai import OpenAILLMAdapter
from llm_wiki.ports.configuration import ConfigurationPort
from llm_wiki.ports.llm import LLMPort


def select_llm_provider(config: ConfigurationPort) -> LLMPort:
    """Apply ADR-004 / S11 selection; raise ProviderUnavailableError if none."""
    override = config.provider_override

    if override == "anthropic":
        if config.anthropic_api_key is None:
            raise ProviderUnavailableError(
                "Anthropic provider requested but ANTHROPIC_API_KEY is not set."
            )
        return AnthropicLLMAdapter(config)

    if override == "ollama":
        return OllamaLLMAdapter(config)

    if override == "openai":
        if config.openai_api_key is None:
            raise ProviderUnavailableError(
                "OpenAI provider requested but OPENAI_API_KEY is not set."
            )
        return OpenAILLMAdapter(config)

    ollama = OllamaLLMAdapter(config)
    if ollama.is_available():
        return ollama

    if config.openai_api_key is not None:
        return OpenAILLMAdapter(config)

    raise ProviderUnavailableError()
