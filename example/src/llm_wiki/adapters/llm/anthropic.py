"""Anthropic LLM adapter via official SDK (ADR-004 / S2-6)."""

from __future__ import annotations

import logging

from anthropic import Anthropic

from llm_wiki.ports.configuration import ConfigurationPort

logger = logging.getLogger(__name__)


class AnthropicLLMAdapter:
    """Anthropic messages API through the official Python SDK."""

    def __init__(
        self,
        config: ConfigurationPort,
        *,
        client: Anthropic | None = None,
    ) -> None:
        self._config = config
        if client is not None:
            self._client = client
        else:
            api_key = config.anthropic_api_key
            if api_key is None:
                raise ValueError("Anthropic adapter requires anthropic_api_key")
            self._client = Anthropic(api_key=api_key)

    def is_available(self) -> bool:
        return self._config.anthropic_api_key is not None

    def complete(self, prompt: str, *, system: str | None = None) -> str:
        logger.debug("Anthropic complete model=%s", self._config.anthropic_model)
        kwargs: dict[str, object] = {
            "model": self._config.anthropic_model,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system is not None:
            kwargs["system"] = system
        response = self._client.messages.create(**kwargs)
        for block in response.content:
            if block.type == "text":
                return block.text
        raise ValueError("Anthropic response missing text block")
