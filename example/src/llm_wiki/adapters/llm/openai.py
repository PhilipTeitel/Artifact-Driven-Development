"""OpenAI LLM adapter via official SDK (ADR-004 / S2-6)."""

from __future__ import annotations

import logging

from openai import OpenAI

from llm_wiki.ports.configuration import ConfigurationPort

logger = logging.getLogger(__name__)


class OpenAILLMAdapter:
    """OpenAI chat completions through the official Python SDK."""

    def __init__(
        self,
        config: ConfigurationPort,
        *,
        client: OpenAI | None = None,
    ) -> None:
        self._config = config
        if client is not None:
            self._client = client
        else:
            api_key = config.openai_api_key
            if api_key is None:
                raise ValueError("OpenAI adapter requires openai_api_key")
            self._client = OpenAI(api_key=api_key)

    def is_available(self) -> bool:
        return self._config.openai_api_key is not None

    def complete(self, prompt: str, *, system: str | None = None) -> str:
        messages: list[dict[str, str]] = []
        if system is not None:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        logger.debug("OpenAI complete model=%s", self._config.openai_model)
        response = self._client.chat.completions.create(
            model=self._config.openai_model,
            messages=messages,
        )
        choice = response.choices[0]
        content = choice.message.content
        if content is None:
            raise ValueError("OpenAI response missing message content")
        return content
